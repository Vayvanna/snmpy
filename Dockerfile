FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

ENV http_proxy=$HTTP_PROXY
ENV https_proxy=$HTTPS_PROXY
ENV no_proxy=$NO_PROXY

RUN pip install --no-cache-dir -r requirements.txt
# RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y iputils-ping vim curl && rm -rf /var/lib/apt/lists/*


COPY . . 

EXPOSE 8000
CMD ["flask", "run", "--host=0.0.0.0", "--reload", "--port=8000"]
# CMD ["python","run.py"]
