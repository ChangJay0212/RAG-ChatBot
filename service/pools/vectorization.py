# -----------Load embedding model---------------
#            For text embedding


# ------------Other---------------
from typing import Literal

# from llama_index.core import StorageContext, VectorStoreIndex
# from core.handler.rag.document_embedding import DocumentEmb
# from core.handler.rag.img_embedding import ImgEmb
#            For image embedding
# from core.models.clip import ClipModel
from core.models.minillm import MinillmModel

# from core.vec_db.faiss.data import Process as ImgPrpcess
# from core.vec_db.faiss.main import Operator as Faiss
# -----------Data pre-process---------------
from core.vec_db.pgvector.data import Process as PdfPrpcess

# ------------Load Vector DB------------------
from core.vec_db.pgvector.main import Operator as PgvecDB


class VectorizationService:
    """
    Service for vectorizing documents and images.

    This class provides methods to process and vectorize PDF documents and images,
    then save the vectorized data into vector databases.

    Methods:
        run(data_folder: str, types: Literal["pdf", "img"] = "pdf") -> None:
            Process and vectorize the data in the specified folder based on the type.
    """

    # def __init__(
    #     self, text_emb_model: MinillmModel, img_emb_model: ClipModel, recreate: bool
    # ) -> None:
    def __init__(
        self,
        text_emb_model: MinillmModel,
        table_name: str = "rag_data",
        tools: Literal["default", "ai"] = "default",
    ) -> None:
        """
        Initialize the VectorizationService with text embedding model.

        Args:
            text_emb_model (MinillmModel): The text embedding model.
            table_name (str): Name of the table in the vector database.
            tools (Literal["default", "ai"]): Tools used for data processing.
        """
        # self.text_emb_service = DocumentEmb(model=text_emb_model)
        self.text_emb = text_emb_model
        # self.img_emb_service = ImgEmb(model=img_emb_model)

        self.pdf_coverter = PdfPrpcess(tools=tools)
        # self.img_coverter = ImgPrpcess()
        self.pgvec_db = PgvecDB(table_name=table_name)
        # self.faiss = Faiss()

    def run(self, data_folder) -> None:
        """
        Process and vectorize the data in the specified folder based on the type.

        Args:
            data_folder (str): Path to the folder containing data.

        Raises:
            TypeError: If the operate type is not supported.
        """
        # if operate == "pdf":
        document_splitter, document = self.pdf_coverter.run(data_folder=data_folder)
        nodes = document_splitter.get_nodes_from_documents(document)
        for i, node in enumerate(nodes):
            vector = self.text_emb.run(data=node.text)
            node.embedding = vector
            print("*" * 10, "\n")
            print(node.text)

        # elif operate == "img":
        #     dataset = self.img_coverter.run(data_folder=data_folder)
        #     dataset_emb = self.img_emb_service.run(dataset=dataset)
        #     self.faiss.save(dataset=dataset_emb)

        # else:
        #     raise TypeError("Not support data type!")
        self.pgvec_db.add(nodes=nodes)
