import os

from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url

connection_string = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@host.docker.internal:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
db_name = "postgres"

# --------connect vec db---------------
url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="rag_data",
    embed_dim=384,  # embedding dimension
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)
# --------load embedding model---------------
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


filters = MetadataFilters(
    filters=[
        MetadataFilter(key="fixes", value="5680", operator="contains"),
    ]
)
index = VectorStoreIndex.from_vector_store(
    embed_model=embed_model, vector_store=vector_store
)
retriever = index.as_retriever(
    # vector_store_query_mode="hybrid",
    similarity_top_k=2,
    vector_store_kwargs={"hnsw_ef_search": 40},
    # filters=filters,
)
retrieved_nodes = retriever.retrieve("3ME3?")

for node in retrieved_nodes:
    print(node.text)
