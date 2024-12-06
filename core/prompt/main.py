from typing import List, Union

from jinja2 import Template

from tools.logger import config_logger

# init log
LOGGER = config_logger(
    log_name="prompt.log",
    logger_name="prompt",
    default_folder="./log",
    write_mode="w",
    level="debug",
)
import llama_index.core.instrumentation as instrument

dispatcher = instrument.get_dispatcher(__name__)


class PromptEngineerService:
    """
    Prompt engineering service.

    This class provides functionality to generate prompts for various purposes such as
    conversation history summarization and generating answers to user questions.

    Methods:
        
        generate(
            retrieval: Union[str, bool],
            prompt: str,
            instruction: Union[List[str], None] = None
        ) -> List[ChatMessage]:
            Generate a prompt based on conversation history, retrieval information, and user question.
    """

    def __init__(self) -> None:
        """
        Initialize the Service with a chat prompt builder and predefined templates.
        """
        # self.builder = PromptTemplate()

        self.template = {
            "chat": """
If you are not sure about the answer or do not have enough information, please answer "i don't know." 

## Context Information

{% if retriever_info %}
Retriever's Information:
{{ retriever_info }}
{% endif %}

## Question and Answer

Question: {{ question }}

Answer:
"""}
        LOGGER.info("Success init prompt !")
    def _package(self,retrieval: Union[str, bool],
        prompt: str,
        instruction: Union[list, None] = None,):
        prompt_package = []
        if instruction:
            if isinstance(instruction,list):
                for command in instruction:
                    if isinstance(command,str):
                        prompt_package.append({"role": "system", "content": command})
                    else:
                        LOGGER.warning("Instruction insert error! skip insert!")
            else:
                prompt_package.append({"role": "system", "content": instruction})

        # if retrieval:
        #     prompt_package.append({"role": "assistant", "content": retrieval})
        
        if prompt:
            prompt_package.append({"role": "user", "content": prompt})
        
        return prompt_package
    
    @dispatcher.span
    def generate(
        self,
        retrieval: Union[str, bool],
        question: str,
        instruction: Union[list, None] = None,
    ) -> str:
        """
        Generate a prompt based on conversation history, retrieval information, and user question.

        Args:
            retrieval (Union[str, bool]): Information retrieved from a database.
            question (str): User question.
            instruction (Union[List[str], None], optional): System instructions. Defaults to None.

        Returns:
            str: The generated prompt for answering the user question.
        """
        template = Template(self.template["chat"])
        prompt = template.render(
            retriever_info=retrieval,
            question=question,
        )
        prompt = self._package(retrieval=retrieval,prompt=prompt,instruction=instruction)
        return prompt


if __name__ == "__main__":
    instruction = "Be kind!"
    retrieval = "3ME3 is a human name!"
    question = "what is 3ME3"
    prompt_service = PromptEngineerService()
    prompt = prompt_service.generate(retrieval=retrieval,question=question,instruction=instruction)
    print(prompt)
