FROM pytorch/pytorch:2.1.1-cuda12.1-cudnn8-devel

WORKDIR /workspace

COPY ["entrypoint", "/usr/bin/"]

COPY requirements.txt /workspace/requirements.txt

RUN chmod u+x /usr/bin/entrypoint

RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r /workspace/requirements.txt


ENTRYPOINT ["entrypoint"]