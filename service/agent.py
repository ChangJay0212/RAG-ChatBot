from core.handler.text_to_text import GenText
from core.models.pattern import (
    Text2Text,
    TextEmbedding,
)
from core.prompt.main import PromptEngineerService
from tools.logger import config_logger

from .pools.retriever import RetrieverService


class Agent:
    """
    Agent class for handling chat interactions and integrating various services.

    This class uses text generation,and retrieval services to process chat prompts and generate responses.

    Methods:
        chat(prompt: str, file: Optional[Image.Image] = None) -> str:
            Handle chat prompt with optional image input and generate a response.
    """

    def __init__(
        self,
        gen_text_model: Text2Text,
        text_emb_model: TextEmbedding,
    ) -> None:
        """
        Initialize the Agent with various models and services.

        Args:
            gen_text_model (Text2Text): The text generation model.
            text_emb_model (TextEmbedding): The text embedding model.

        """

        self.gentxt_service = GenText(model=gen_text_model)

        self.retriever_service = RetrieverService(text_emb_model=text_emb_model)

        self.prompt_engineer = PromptEngineerService()

    def chat(
        self,
        log: config_logger,
        prompt: str,
    ) -> str:
        """
        Handle chat prompt to generate a response.

        Args:
            log (config_logger): logger.
            prompt (str): The chat prompt from the user.

        Returns:
            str: The generated response from the agent.
        """

        log.info("Start chat!")
        log.info(f"User prompt:'{prompt}'.")

        retriever = self.retriever_service.search(data=prompt)
        log.info(f"Retriever. :'{retriever}'.")
        final_prompt = self.prompt_engineer.generate(
            retrieval=retriever,
            question=prompt,
            instruction=None,
        )
        log.info(f"Final prompt. :'{final_prompt}'.")
        response = self.gentxt_service.run(prompt=final_prompt)
        log.info(f"Response. :'{response}'.")

        return response
