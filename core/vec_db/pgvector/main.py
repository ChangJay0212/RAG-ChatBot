import os
from typing import List

from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url

os.environ["PG_CONN_STR"] = (
    f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@postgres:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
)
import logging

from tools.logger import config_logger

# Initialize logger
LOGGER = config_logger(
    log_name="pgvec.log",
    logger_name="pgvec",
    default_folder="./log",
    write_mode="w",
    level="debug",
)


class Operator:
    """
    Pgvector operator for managing and retrieving documents in a vector database.

    This operator allows initializing the vector database, saving documents,
    setting up the retriever, and searching for documents based on query embeddings.

    Attributes:
        vector_store (PGVectorStore): The vector store for managing vector embeddings.

    Methods:
        add(nodes: list) -> None:
            Add nodes to the vector database.

        save(documents: list) -> None:
            Save the documents to the vector database.

        set_retriever(top_k: int = 2) -> None:
            Set the retriever for querying the vector database.

        search(query_embedding: List[float], filters: dict = {"operator": "AND", "conditions": [{"field": "meta.privacy", "operator": "!=", "value": "1"}]}) -> List[float]:
            Retrieve documents from the vector database based on query embeddings.
    """

    def __init__(
        self,
        table_name: str = "rag_data",
        embedding_dimension: int = 384,
        hnsw_kwargs: dict = {
            "hnsw_m": 16,
            "hnsw_ef_construction": 64,
            "hnsw_ef_search": 40,
            "hnsw_dist_method": "vector_cosine_ops",
        },
    ) -> None:
        """
        Initialize the Pgvector operator.

        Args:
            table_name (str, optional): The name of the table in the vector database. Defaults to "rag_data".
            embedding_dimension (int, optional): Dimension of the embedding vectors. Defaults to 384.
            hnsw_kwargs (dict, optional): Parameters for HNSW search. Defaults to specified dictionary.
        """

        logging.info("Initializing pgvector...")
        # Initializing the VectorStore
        connection_string = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@postgres:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
        db_name = "postgres"
        url = make_url(connection_string)
        self.vector_store = PGVectorStore.from_params(
            database=db_name,
            host=url.host,
            password=url.password,
            port=url.port,
            user=url.username,
            table_name=table_name,
            embed_dim=embedding_dimension,  # embedding dimension
            hnsw_kwargs=hnsw_kwargs,
        )
        LOGGER.info(
            f"Success initializing pgvector.\nTable name: {table_name}\nEmbedding dimension: {embedding_dimension}\nHNSW parameters: {hnsw_kwargs}"
        )

    def add(self, nodes: list) -> None:
        """
        Add nodes to the vector database.

        Args:
            nodes (list): A list of nodes to add to the vector database.
        """
        self.vector_store.add(nodes=nodes)
        LOGGER.info(f"Added {len(nodes)} nodes to the vector database.")
