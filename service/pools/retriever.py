from llama_index.core import VectorStoreIndex

from core.models.minillm import MinillmModel
from core.vec_db.pgvector.main import Operator as PgvecDB


class RetrieverService:
    """
    Service for retrieving data from databases .

    Attributes:
        text_emb_service (TextEmb): Service for generating text embeddings.
        pgvec_db (PgvecDB): Vector database for text data retrieval.

    Methods:
        search(data: str) -> str:
            Search data from the database .
    """

    def __init__(self, text_emb_model: MinillmModel) -> None:
        """
        Initialize the RetrieverService with text .

        Args:
            text_emb_model (MinillmModel): The text embedding model.
        """
        self.text_emb = text_emb_model

        self.pgvec_db = PgvecDB()

        self.pg_retriver = self._init_retriever(
            emb_model=self.text_emb, vector_store=self.pgvec_db.vector_store
        )

    def _init_retriever(self, emb_model, vector_store):
        index = VectorStoreIndex.from_vector_store(
            embed_model=emb_model, vector_store=vector_store
        )
        retriever = index.as_retriever(
            # vector_store_query_mode="hybrid",
            similarity_top_k=10,
            vector_store_kwargs={"hnsw_ef_search": 40},
            # filters=filters,
        )
        return retriever

    def _search_from_pgvecdb(self, data: str) -> str:
        """
        Search for text data in the PgvecDB.

        Args:
            data (str): The text data to be searched.

        Returns:
            str: The content of the top-ranked document if found, otherwise None.
        """
        # filters = MetadataFilters(
        #     filters=[
        #         MetadataFilter(key="fixes", value="5680", operator="contains"),
        #     ]
        # )
        retrieved_nodes = self.pg_retriver.retrieve(data)
        return "".join(node.text for node in retrieved_nodes)

    def search(self, data: str) -> str:
        """
        Search data from the database .

        Args:
            data (str): The data to be searched.

        Returns:
            str: The content or description of the top-ranked result.

        """

        retriever_result = self._search_from_pgvecdb(data=data)

        return retriever_result


if __name__ == "__main__":
    from core.models.minillm import MinillmModel

    test_data = "what is EGPS-3401"
    model = MinillmModel(host="10.204.16.50")
    retriever_service = RetrieverService(text_emb_model=model)
    result = retriever_service.search(data=test_data)
    print(result)
