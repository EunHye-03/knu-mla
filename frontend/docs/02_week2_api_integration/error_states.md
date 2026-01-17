# Error States

## HTTP Codes
- **400 Bad Request**: Missing required fields or invalid file type.
- **413 Payload Too Large**: File size > 10MB.
- **429 Too Many Requests**: Rate limit exceeded.
- **500 Internal Server Error**: AI service failure.

## Client Handling
- **4xx**: Show specific error message toast ("Please upload a PDF").
- **5xx**: Show generic error ("Service busy, try again").
