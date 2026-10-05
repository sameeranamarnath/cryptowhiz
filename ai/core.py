"""Config, model clients and Qdrant access for the crypto research service."""

from functools import lru_cache
from typing import Any

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic_settings import BaseSettings, SettingsConfigDict
from qdrant_client import QdrantClient, models


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_base_url: str = "http://vllm:8000/v1"
    llm_api_key: str = "local-vllm"
    llm_model: str = "Qwen/Qwen3-32B"

    embed_base_url: str = "http://vllm-embed:8000/v1"
    embed_model: str = "BAAI/bge-m3"
    embed_dim: int = 1024

    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "crypto_news"

    coingecko_base: str = "https://api.coingecko.com/api/v3"
    candles_days: int = 180
    news_top_k: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()


def chat_model(temperature: float = 0.2, max_tokens: int = 1200) -> ChatOpenAI:
    s = get_settings()
    return ChatOpenAI(
        model=s.llm_model,
        base_url=s.llm_base_url,
        api_key=s.llm_api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        max_retries=2,
        timeout=120,
    )


def embed_model() -> OpenAIEmbeddings:
    s = get_settings()
    return OpenAIEmbeddings(
        model=s.embed_model,
        base_url=s.embed_base_url,
        api_key=s.llm_api_key,
        check_embedding_ctx_length=False,
    )


def qdrant() -> QdrantClient:
    s = get_settings()
    return QdrantClient(url=s.qdrant_url, api_key=s.qdrant_api_key)


def ensure_collection() -> str:
    s = get_settings()
    c = qdrant()
    if not c.collection_exists(s.qdrant_collection):
        c.create_collection(
            collection_name=s.qdrant_collection,
            vectors_config=models.VectorParams(
                size=s.embed_dim, distance=models.Distance.COSINE
            ),
        )
    return s.qdrant_collection


def upsert_notes(notes: list[dict[str, Any]]) -> int:
    """Store news/notes for later retrieval. Each note needs 'text'; the rest is payload."""
    collection = ensure_collection()
    texts = [n["text"] for n in notes]
    vectors = embed_model().embed_documents(texts)
    c = qdrant()
    start = c.count(collection_name=collection).count
    points = [
        models.PointStruct(
            id=start + i,
            vector=v,
            payload={k: val for k, val in n.items() if k != "text"} | {"text": t},
        )
        for i, (n, t, v) in enumerate(zip(notes, texts, vectors))
    ]
    c.upsert(collection_name=collection, points=points)
    return len(points)


def search_notes(query: str, symbol: str | None = None, top_k: int | None = None) -> list[dict[str, Any]]:
    s = get_settings()
    collection = ensure_collection()
    query_filter = None
    if symbol:
        query_filter = models.Filter(
            must=[models.FieldCondition(key="symbol", match=models.MatchValue(value=symbol.lower()))]
        )
    hits = qdrant().search(
        collection_name=collection,
        query_vector=embed_model().embed_query(query),
        query_filter=query_filter,
        limit=top_k or s.news_top_k,
        with_payload=True,
    )
    return [{"score": h.score, **(h.payload or {})} for h in hits]
