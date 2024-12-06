import json

import httpx
from utils.chat import get_rag_route
from utils.connect import get_rag_host, get_rag_port


class RagHandler:
    def __init__(self) -> None:
        self.host = get_rag_host()
        self.port = get_rag_port()
        self.chat_api = get_rag_route(self.host, self.port)
        self.current_messages = []

    def chat(self, username: str, department: str, prompt: str):
        params = {"username": username.lower(), "department": department.lower()}
        form_data = {"prompt": prompt}

        with httpx.stream(
            "POST",
            self.chat_api,
            params=params,
            data=form_data,
            timeout=30,
            follow_redirects=True,
        ) as response:
            if response.status_code == 200:
                message = ""
                for chunk in response.iter_text():
                    message += chunk
                try:
                    message_json = json.loads(message)
                    return message_json["message"]
                except:
                    pass
            else:
                raise ValueError(
                    f"Unexpected response status code: {response.status_code}"
                )

    # def stream_chat(self) -> Generator[str] | None:
    #     if self.current_messages == []:
    #         print("There is no current messages")
    #         return
    #     data = OllamaRequestData(
    #         model=self.model, messages=self.current_messages
    #     ).model_dump()
    #     with httpx.stream("POST", url=self.chat_api, json=data, timeout=30) as response:
    #         if response.headers.get("Transfer-Encoding") == "chunked":
    #             for chunk in response.iter_lines():
    #                 yield json.loads(chunk)["message"]["content"]
    #         else:
    #             raise RuntimeError(json.loads(response.read().decode("utf-8")))

    #     self.current_messages.clear()
