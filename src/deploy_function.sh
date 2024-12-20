#!/bin/bash

# Обновление версии функции с загрузкой исходного кода
yc serverless function version create \
  --function-name github-parser \
  --runtime python312 \
  --entrypoint github_parser.parse_and_save \
  --memory 128m \
  --execution-timeout 60s \
  --source-path ./function.zip \
  --environment DB_HOST=localhost,DB_USER=maslova,DB_PASSWORD=maslova_pw,DB_NAME=github_data

# Создание триггера (таймер)
yc serverless trigger create timer \
  --name github-parser-trigger \
  --invoke-function-name github-parser \
  --cron-expression "0 * ? * * *"



