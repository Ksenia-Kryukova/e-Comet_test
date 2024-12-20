#!/bin/bash

# Создание серверной функции
yc serverless function create \
  --name github-parser \
  --runtime python311 \
  --entrypoint index.handler \
  --memory 128m \
  --execution-timeout 60s

# Создание версии функции с загрузкой исходного кода
yc serverless function version create \
  --function-name github-parser \
  --source-path ./function.zip \
  --environment DB_HOST=localhost,DB_USER=maslova,DB_PASSWORD=maslova_pw,DB_NAME=github_data

# Создание триггера для регулярного запуска
yc serverless function trigger create \
  --name github-parser-trigger \
  --function-name github-parser \
  --schedule "every 6 hours"
