# ----------------emb test-----------
# from core.handler.embedding.text_embedding import TextEmb
# from core.models.minillm import MinillmModel

# test_data = "test!"
# model = MinillmModel(host="10.204.16.75")


# text_emb = TextEmb(model=model)
# emb = text_emb.run(data=test_data)
# print(emb)

# ------------------gen text test ---------------
# from core.models.ollama import Llama31Model
# from core.handler.text_to_text import GenText
# prompt = [
#             {"role": "system", "content": "Be kind!"},
#             {"role": "user", "content": "How r u?"},
#         ]
# model = Llama31Model(host="10.204.16.50")
# txtgen = GenText(model=model)
# gen_text = txtgen.run(prompt=prompt)
# print(gen_text)

# ------------------prompt test ---------------
# from core.prompt.main import PromptEngineerService
# instruction = "Be kind!"
# retrieval = "3ME3 is a human name!"
# question = "what is 3ME3"
# prompt_service = PromptEngineerService()
# prompt = prompt_service.generate(retrieval=retrieval,question=question,instruction=instruction)
# print(prompt)


# ------------------MinillmModel RetrieverService test ---------------
# from core.models.minillm import MinillmModel
# from service.pools.retriever import RetrieverService
# test_data = "what is EGPS-3401"
# model = MinillmModel(host="10.204.16.50")

# retriever_service = RetrieverService(text_emb_model=model)
# result = retriever_service.search(data=test_data)
# print(result)
# ------------------prompt with gen text test ---------------
# from core.prompt.main import PromptEngineerService
# from core.models.ollama import Llama31Model
# from core.handler.text_to_text import GenText
# instruction = "Be kind!"
# retrieval = "3ME3 is a camera!"
# question = "Is 3ME3 is a camera?"
# prompt_service = PromptEngineerService()
# prompt = prompt_service.generate(retrieval=retrieval,question=question,instruction=instruction)
# model = Llama31Model(host="10.204.16.50")
# txtgen = GenText(model=model)
# print(prompt)
# gen_text = txtgen.run(prompt=prompt)
# print(gen_text)
# ------------------Retriever with Prompt service with Generate model test ---------------
# from core.models.minillm import MinillmModel
# from service.pools.retriever import RetrieverService
# from core.prompt.main import PromptEngineerService
# from core.models.ollama import Llama31Model
# from core.handler.text_to_text import GenText

# test_data = "what is EGPS-3401"
# model = MinillmModel(host="10.204.16.50")
# retriever_service = RetrieverService(text_emb_model=model)
# instruction = "Be kind!"
# retrieval = retriever_service.search(data=test_data)
# question = "what is EGPS-3401?"
# prompt_service = PromptEngineerService()
# prompt = prompt_service.generate(retrieval=retrieval,question=question,instruction=instruction)
# model = Llama31Model(host="10.204.16.50")
# txtgen = GenText(model=model)
# gen_text = txtgen.run(prompt=prompt)
# print(gen_text)
# ------------------Agent test ---------------

# from core.handler.text_to_text import GenText
# from core.models.minillm import MinillmModel
# from core.models.ollama import Llama31Model
# from core.prompt.main import PromptEngineerService
# from service.agent import Agent
# from service.pools.retriever import RetrieverService
# from tools.user_register import UserHandler

# user_handler = UserHandler()


# model_server_url = "10.204.16.75"
# username = "jay"
# department = "ipa"


# prompt = "what is EGPS-3401"
# text_emb_model = MinillmModel(host=model_server_url)
# gen_text_model = Llama31Model(host=model_server_url)
# agent = Agent(gen_text_model=gen_text_model, text_emb_model=text_emb_model)
# llm_answer = agent.chat(
#     log=user_handler.get(username=username, department=department), prompt=prompt
# )
# print(llm_answer)
# from core.models import Llama31Model

# prompt = [
#     {"role": "system", "content": "Be kind!"},
#     {"role": "user", "content": "How r u?"},
# ]
# gen_text = ""
# model = Llama31Model(host="10.204.16.75")
# for prompt in model.run(prompt=prompt):
#     if isinstance(prompt, str):
#         gen_text += prompt  # Assume result is a full string
# print(gen_text)

# import os


# def find_all_pdfs(root_folder):
#     pdf_files = []
#     for root, _, files in os.walk(root_folder):
#         for file in files:
#             if file.lower().endswith(".pdf"):
#                 pdf_files.append(os.path.join(root, file))
#     return pdf_files


# # 使用方法
# root_folder = "./data/10/"  # 這裡替換成你想要搜尋的主資料夾路徑
# pdf_files = find_all_pdfs(root_folder)


# def extract_specific_part(file_path):
#     # 提取檔案名稱，不包含副檔名
#     filename = os.path.basename(file_path)
#     name_without_ext = os.path.splitext(filename)[0]

#     # 將檔名以底線分割，擷取出所需部分
#     parts = name_without_ext.split("_")
#     if len(parts) >= 2:
#         specific_part = f"{parts[0]}_{parts[1]}"
#         return specific_part
#     else:
#         return None


# # 列出找到的 PDF 檔案
# for pdf in pdf_files:
#     print(extract_specific_part(pdf))
