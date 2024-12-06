from typing import List, Optional

import httpx
from llama_index.core.base.embeddings.base import BaseEmbedding
from pydantic import PrivateAttr

from tools.logger import config_logger

from .pattern import TextEmbedding

# init log
LOGGER = config_logger(
    log_name="minillm.log",
    logger_name="minillm",
    default_folder="./log",
    write_mode="w",
    level="debug",
)


class MinillmModel(BaseEmbedding, TextEmbedding):
    _ollama_url: str = PrivateAttr()

    def __init__(
        self,
        model_name: str = "all-minilm:latest",
        host: str = "10.204.16.75",
        port: int = 11434,
    ):
        super().__init__(
            model_name=model_name,
        )

        TextEmbedding.__init__(self, model_name=model_name)
        self.model_name = model_name
        self._ollama_url = f"http://{host}:{str(port)}/api/"

        self._pull_model()

    def _pull_model(self):
        data = {"name": self.model_name}

        with httpx.stream(
            "POST", url=self._ollama_url + "pull", json=data, timeout=None
        ) as response:
            if (
                response.status_code == 200
                and response.headers.get("Transfer-Encoding") == "chunked"
            ):
                LOGGER.info("Response is a streaming response")

                for chunk in response.iter_lines():
                    LOGGER.info(chunk)

    def _load_model(self):
        data = {"model": self.model_name, "keep_alive": -1}
        with httpx.Client() as client:
            response = client.post(
                url=self._ollama_url + "embeddings", json=data, timeout=None
            )

        if response.status_code != 200:
            LOGGER.error(f"{self.model_name} can not loaded!")
            raise RuntimeError
        LOGGER.info(f"Success init {self.model_name}!")

    def _release_model(self):
        data = {"model": self.model_name, "keep_alive": 0}
        with httpx.Client() as client:
            response = client.post(
                url=self._ollama_url + "embeddings", json=data, timeout=None
            )

        if response.status_code != 200:
            LOGGER.error(f"{self.model_name} can not released!")
        LOGGER.info(f"Success release {self.model_name}!")

    @classmethod
    def class_name(cls) -> str:
        return "HuggingFaceEmbedding"

    def _embed(
        self,
        sentences: List[str],
        prompt_name: Optional[str] = None,
    ) -> List[List[float]]:
        return self.run(data=sentences)

    def _get_query_embedding(self, query: str) -> List[float]:
        """Generates Embeddings for Query.

        Args:
            query (str): Query text/sentence

        Returns:
            List[float]: numpy array of embeddings
        """
        return self._embed(query, prompt_name="query")

    async def _aget_query_embedding(self, query: str) -> List[float]:
        """Generates Embeddings for Query Asynchronously.

        Args:
            query (str): Query text/sentence

        Returns:
            List[float]: numpy array of embeddings
        """
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Generates Embeddings for text Asynchronously.

        Args:
            text (str): Text/Sentence

        Returns:
            List[float]: numpy array of embeddings
        """
        return self._get_text_embedding(text)

    def _get_text_embedding(self, text: str) -> List[float]:
        """Generates Embeddings for text.

        Args:
            text (str): Text/sentences

        Returns:
            List[float]: numpy array of embeddings
        """
        return self._embed(text, prompt_name="text")

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates Embeddings for text.

        Args:
            texts (List[str]): Texts / Sentences

        Returns:
            List[List[float]]: numpy array of embeddings
        """
        return self._embed(texts, prompt_name="text")

    def run(self, data: str) -> list:
        request_data = {"model": self.model_name, "input": data}

        with httpx.Client() as client:
            response = client.post(
                url=self._ollama_url + "embed", json=request_data, timeout=None
            )

        if response.status_code == 200:
            content = response.json()
            result = content["embeddings"][0]
        return result


if __name__ == "__main__":
    model = MinillmModel(host="10.204.16.50")
    emb = model.run(data="test!")
    print(emb)
