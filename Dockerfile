FROM omerxx/awscli:alpine

WORKDIR /app

COPY *.py requirements.txt /app/

RUN apk -Uuv add py-pip && \
    pip install -r requirements.txt && \
    apk --purge -v del py-pip && \
    rm /var/cache/apk/*


CMD ["python", "/app/plugin.py"]
