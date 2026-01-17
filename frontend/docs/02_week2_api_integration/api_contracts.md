# API Contracts

## Base URL
`http://localhost:8000/api/v1`

## Endpoints

### POST /translate
- **Body**: `{ "text": "string", "target_lang": "string" }`
- **Response**: `{ "content": "translated text..." }`

### POST /summarize
- **Body**: `{ "text": "string" }`
- **Response**: `{ "summary": "summary text..." }`

### POST /explain
- **Body**: `{ "term": "string" }`
- **Response**: `{ "explanation": "definition..." }`

### POST /audio/stt
- **Body**: `FormData("file": blob)`
- **Response**: `{ "text": "transcribed text" }`
