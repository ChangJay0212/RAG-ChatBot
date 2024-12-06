import io
import json
import os
from typing import Literal, Optional

import httpx
import llama_index.core
from fastapi import (
    BackgroundTasks,
    FastAPI,
    File,
    Form,
    Response,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel

from core.models import Llama31Model, MinillmModel
from service.agent import Agent
from tools.logger import config_logger
from tools.redis_handler import RedisNotifier
from tools.user_register import UserHandler

model_server_url = "10.204.16.75"
# --------------Connect to phoenix, start-----------------------
os.environ["PHOENIX_HOST"] = "phoenix"  #
os.environ["PHOENIX_PORT"] = "6006"


llama_index.core.set_global_handler(
    "arize_phoenix",
    endpoint=f"http://{os.environ['PHOENIX_HOST']}:{os.environ['PHOENIX_PORT']}/v1/traces",
)
# --------------Connect to phoenix , end-----------------------


# ----------------------Check feedback data ,start----------------------
class Result(BaseModel):
    label: Literal["thumbs-up", "thumbs-down"]
    score: float
    explanation: str


class FeedBack(BaseModel):
    span_id: str
    name: str = "user feedback"
    annotator_kind: str = "HUMAN"
    result: Result
    metadata: dict


# ----------------------Check feedback data ,end----------------------

# feedback call api
client = httpx.Client()
app = FastAPI()
user_handler = UserHandler()

# init log
logger = config_logger(
    log_name="system.log",
    logger_name="system",
    default_folder="./log",
    write_mode="w",
    level="debug",
)
redis = RedisNotifier()

# Init model
gen_text_model = Llama31Model(host=model_server_url, redis=redis)
logger.info(
    f"Success init model to Gen text. model name = '{gen_text_model.model_name}'"
)
text_emb_model = MinillmModel(host=model_server_url)
logger.info(
    f"Success init model to Embedding text. model name = '{text_emb_model.model_name}'"
)

# init Service
agent = Agent(gen_text_model=gen_text_model, text_emb_model=text_emb_model)
logger.info("Success init Agent")


@app.post("/chat/", tags=["Chat"])
async def chat(
    username: str,
    department: str,
    file: Optional[UploadFile] = File(None),
    prompt: Optional[str] = Form(None),
):
    response = {}
    if not user_handler.check(username=username, department=department):
        response["message"] = f"User '{username}' has not registered yet."
        return response

    logger.info(f"user : '{username}'")
    logger.info(f"user prompt : {prompt}")
    # try:
    #     contents = await file.read()
    #     image = Image.open(io.BytesIO(contents))
    # except:
    #     image = None

    llm_answer = agent.chat(
        log=user_handler.get(username=username, department=department), prompt=prompt
    )
    span_id = redis.get_value()

    response["message"] = llm_answer
    try:
        response["span_id"] = span_id.decode("utf-8")

    except:
        response["span_id"] = None
    logger.info(f"Chat bot answer : {response}")
    print(response)
    return JSONResponse(content=response)


@app.post("/feedback/")
def feedback(feedback: FeedBack):
    annotation_payload = {
        "data": [
            {
                "span_id": feedback.span_id,
                "name": feedback.name,
                "annotator_kind": feedback.annotator_kind.upper(),
                "result": {
                    "label": feedback.result.label,
                    "score": feedback.result.score,
                    "explanation": feedback.result.explanation,
                },
                "metadata": feedback.metadata,
            }
        ]
    }

    client.post(
        f"http://{os.environ['PHOENIX_HOST']}:{os.environ['PHOENIX_PORT']}/v1/span_annotations?sync=false",
        json=annotation_payload,
    )
    return JSONResponse(content=annotation_payload)


@app.post("/submit/")
def submit(
    username: str,
    department: str,
):
    response = {}
    print(user_handler.check(username=username, department=department))
    if user_handler.check(username=username, department=department):
        response["message"] = f"User: '{username}' has been registered !"
        return JSONResponse(content=response)
    user_handler.register(username=username, department=department)

    response["message"] = (
        f"User '{username}' , Department : '{department}' successfully registered!"
    )
    return JSONResponse(content=response)


@app.post("/report/")
def report(username: str, department: str, feedback: str):
    response = {}
    if not user_handler.check(username=username, department=department):
        response["message"] = f"User '{username}' has not registered yet."
        return response
    log = user_handler.get(username=username, department=department)
    log.info(f"User feedback : '{feedback}'")

    response["message"] = (
        f"User '{username}' , Department : '{department}' successfully send feedback!"
    )
    return JSONResponse(content=response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
