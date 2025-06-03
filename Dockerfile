FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
# RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y iputils-ping vim curl && rm -rf /var/lib/apt/lists/*


COPY . . 

EXPOSE 8000
CMD ["flask", "run", "--host=0.0.0.0", "--reload", "--port=8000"]
# CMD ["python","run.py"]