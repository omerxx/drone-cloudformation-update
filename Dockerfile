FROM omerxx/awscli:alpine

WORKDIR /app

COPY plugin.py /app

CMD ["python", "/app/plugin.py"]
