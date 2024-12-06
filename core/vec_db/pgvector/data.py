from pathlib import Path
from typing import Literal

from llama_index.core import SimpleDirectoryReader

# from haystack.components.converters import PyPDFToDocument, TextFileToDocument
from llama_index.core.node_parser import SentenceSplitter

# from llama_index.readers.smart_pdf_loader import SmartPDFLoader
from core.models import Llama31Model
from tools.ai_markdown_reader import AI_PDFLoader

# from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from tools.logger import config_logger
from tools.markdown_splitter import MarkdownSplitterNodeParser

# init log
LOGGER = config_logger(
    log_name="pgvec_data.log",
    logger_name="pgvec_data",
    default_folder="./log",
    write_mode="w",
    level="debug",
)


class Process:
    """
    Perform data preprocessing for RAG (Retrieval-Augmented Generation).

    This class includes tools for converting PDFs to documents, cleaning the documents,
    and splitting them for further processing.

    Attributes:
        reader: Tool for reading PDF files. It can be either an AI-based reader or a simple reader.
        document_splitter: Tool for splitting documents into chunks for easier processing.

    Methods:
        run(data_folder: str, private: bool = False) -> list:
            Preprocess data for RAG, returning the document splitter and processed documents.
    """

    def __init__(self, tools: Literal["default", "ai"] = "default") -> None:
        """
        Initialize the Process class for data preprocessing.

        Args:
            tools (Literal["default", "ai"]): Specify which set of tools to use for data preprocessing. Defaults to "default".
        """
        LOGGER.info("Init pgvector data process...")
        self._init_tools(tools)
        LOGGER.info("Success init pgvector data process...")

    def _init_tools(self, usage_tools: Literal["default", "ai"]):
        """
        Initialize all tools for data processing based on the specified toolset.

        Args:
            usage_tools (Literal["default", "ai"]): The toolset to use for data processing.
        """
        LOGGER.info("Initializing pdf_converter...")
        if usage_tools.lower() == "ai":
            model = Llama31Model(host="10.204.16.75")
            self.reader = AI_PDFLoader(model=model)
            self.document_splitter = MarkdownSplitterNodeParser(separator="#")
        else:
            self.reader = None
            self.document_splitter = SentenceSplitter(
                chunk_size=512,
                chunk_overlap=10,
                paragraph_separator="\n\n\n",  # Separator for paragraphs
                secondary_chunking_regex="[^,.;\u3002\uff1f\uff01]+[,.;\u3002\uff1f\uff01]?",  # Pattern for splitting sentences
                separator=" ",  # Separator for the smallest chunks
            )
        LOGGER.info(
            "Success init document_splitter with settings: chunk_size=512, chunk_overlap=10, paragraph_separator='\n\n\n', secondary_chunking_regex='[^,.;\u3002\uff1f\uff01]+[,.;\u3002\uff1f\uff01]?', separator=' '"
        )

    def _private_setting(self, private: bool = False) -> dict:
        """
        Generate privacy settings based on the private parameter.

        Args:
            private (bool): If True, generates a privacy level 0 setting; otherwise, generates a privacy level 1 setting. Default is False.

        Returns:
            dict: A function that returns privacy settings for a given filename.
        """
        if private:
            return lambda filename: {"file_name": filename, "privacy": 0}
        return lambda filename: {"file_name": filename, "privacy": 1}

    def run(self, data_folder: str, private: bool = False) -> list:
        """
        Preprocess data for RAG by reading, optionally applying privacy settings, and splitting documents.

        Args:
            data_folder (str): The path to the data folder (currently only supports PDF files).
            private (bool): Whether to apply privacy settings to the documents. Default is False.

        Returns:
            list: A list containing the document splitter and processed documents.
        """

        privacy_settings = self._private_setting(private=private)
        if self.reader:
            docs = SimpleDirectoryReader(
                input_dir=data_folder,
                file_metadata=privacy_settings,
                file_extractor={".pdf": self.reader},
                recursive=True,
            ).load_data()
        else:
            docs = SimpleDirectoryReader(
                input_dir=data_folder,
                file_metadata=privacy_settings,
                recursive=True,
            ).load_data()

        return self.document_splitter, docs


if __name__ == "__main__":
    data_handler = Process()
    document_splitter, docs = data_handler.run(data_folder="./data/new_data")
    nodes = document_splitter.get_nodes_from_documents(docs)
    for i, node in enumerate(nodes):
        print(node.text)
