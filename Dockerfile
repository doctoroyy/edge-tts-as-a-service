FROM python:3.9-slim-buster

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh

EXPOSE 5000

CMD ["./start.sh"]
