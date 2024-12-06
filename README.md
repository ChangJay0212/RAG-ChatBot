# Chatbot Service

This chatbot provides RAG (Retrieval-Augmented Generation) functionality, allowing users to easily ask questions. The model used for this service is based on [Ollama](https://github.com/ollama/ollama). The frontend is implemented using [Streamlit](https://github.com/streamlit/streamlit).

## User Usage
![image](/docs/example.gif)

### Start the Service

To start the Chatbot service, use Docker Compose with the provided configuration file:

```bash
docker compose -f ./compose.yaml up -d
# Enter bash 
docker exec -it rag_v1 /bin/bash

```
### Trace the Chat History
To trace the chat history more conveniently, use [Phoenix](https://github.com/Arize-ai/phoenix).
![image](/docs/trace.png)




### Shutdown service
```bash
docker compose down
```

### How to update vector database?
* Follow [Vectorization](/docs/Vectorization.md) to update new data to vector database.

## Other
* [Development readme](/docs/README.DEV.md) 
* [Update map](/docs/UPDATE.md)
* [Todo](/docs/TODO.md)

