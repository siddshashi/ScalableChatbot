#!/bin/sh
ollama serve &  
sleep 2  
ollama pull mistral  
fg  