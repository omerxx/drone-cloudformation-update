FROM omerxx/awscli:alpine

WORKDIR /app

RUN pip install -r requirements.txt

COPY plugin.py /app

CMD ["python", "/app/plugin.py"]
