FROM python:3.13.2-alpine3.20

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "main.py"]