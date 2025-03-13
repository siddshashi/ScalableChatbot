#!/bin/sh
nohup ollama serve &
sleep 10
ollama pull mistral
tail -f /dev/null
