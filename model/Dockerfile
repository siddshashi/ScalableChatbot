FROM ollama/ollama:latest

WORKDIR /app

COPY . .

RUN ollama pull mistral

EXPOSE 11434

CMD ["ollama", "serve"]