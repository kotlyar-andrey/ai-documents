## Инструкция по запуску

### Клонировать репозиторий
<pre>git clone git@github.com:kotlyar-andrey/ai-documents.git
cd ai-documents</pre>

### Создать `.env` файл 
`OPENAI_API_KEY=ваш ключ OpenAi`

### Запустить докер контейнер
`docker compose up --build`

backend будет доступен по адресу `0.0.0.0:8000`  
frontend будет доступ по адресу `localhost:5173` 

## Доступные эндпоинты

### `GET /documents`
получить список всех загруженных документов

### `POST /documents`
загрузка документа `file`. В ответе будет `id` документа и будут установлены куки сессии

### `GET /documents/{id}/summmary`
получить краткое содержимое загруженного ранее документа

### `DELETE /documents/{id}`
удалить документ по его `id`

### `POST /chat`  
отправить `message` с вопросом и получить ответ на основе всех загруженных ранее документов

