import json
from collections.abc import Generator

import httpx
import llama_index.core.instrumentation as instrument
from opentelemetry import trace

from tools.logger import config_logger
from tools.redis_handler import RedisNotifier

from .pattern import Text2Text

dispatcher = instrument.get_dispatcher(__name__)
# init log
LOGGER = config_logger(
    log_name="llama.log",
    logger_name="llama",
    default_folder="./log",
    write_mode="w",
    level="debug",
)


class Llama31Model(Text2Text):
    def __init__(
        self,
        model_name: str = "llama3.1",
        host: str = "localhost",
        port: int = 11434,
        redis: RedisNotifier = None,
    ) -> None:
        super().__init__(model_name)
        self.model_name = model_name
        self.ollama_url = f"http://{host}:{str(port)}/api/"
        self.redis = redis
        # self._pull_model()

    def _pull_model(self):
        data = {"name": self.model_name}

        with httpx.stream(
            "POST", url=self.ollama_url + "pull", json=data, timeout=None
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
                url=self.ollama_url + "generate", json=data, timeout=None
            )

        if response.status_code != 200:
            LOGGER.error(f"{self.model_name} can not loaded!")
            raise RuntimeError
        LOGGER.info(f"Success init {self.model_name}!")

    def _release_model(self):
        data = {"model": self.model_name, "keep_alive": 0}
        with httpx.Client() as client:
            response = client.post(
                url=self.ollama_url + "generate", json=data, timeout=None
            )

        if response.status_code != 200:
            LOGGER.error(f"{self.model_name} can not released!")
        LOGGER.info(f"Success release {self.model_name}!")

    def chat_stream(self, request_data: dict) -> Generator[str]:
        try:
            with httpx.stream(
                "POST", url=self.ollama_url + "chat", json=request_data, timeout=None
            ) as response:
                if response.headers.get("Transfer-Encoding") == "chunked":
                    for chunk in response.iter_lines():
                        yield json.loads(chunk)["message"]["content"]
                else:
                    raise RuntimeError(json.loads(response.read().decode("utf-8")))
        except BaseException as e:
            yield f"Error occurred: {str(e)}\n\n"

    @dispatcher.span
    def run(self, prompt: list, max_tokens: int = 350) -> Generator[str]:
        LOGGER.info(
            f"Input: {[entry['content'] for entry in prompt if entry['role'] == 'user']}"
        )
        request_data = {
            "model": self.model_name,
            "messages": prompt,
            "options": {"num_predict": max_tokens},
        }
        yield from self.chat_stream(request_data=request_data)
        # LOGGER.info(f"Output :{result} , type:{type(result)}")
        current_span = trace.get_current_span()
        span_id = current_span.get_span_context().span_id.to_bytes(8, "big").hex()
        if self.redis:
            self.redis.send(span_id)


if __name__ == "__main__":
    prompt = [
        {"role": "system", "content": "Be kind!"},
        {"role": "user", "content": "How r u?"},
    ]
    gen_text = ""
    model = Llama31Model(host="10.204.16.50")
    for prompt in model.run(prompt=prompt):
        if isinstance(prompt, str):
            gen_text += prompt  # Assume result is a full string
    print(gen_text)
