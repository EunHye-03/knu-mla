# Test Plan

## Unit Tests (Backend)
- Verify `translate()` logic works with mock LLM.
- Verify file parser handles PDF/TXT correctly.

## Integration Tests (Frontend -> Backend)
- **Happy Path**: Send text -> Receive translation.
- **Edge Cases**: Send empty string, Send 100mb file.

## Tools
- **Backend**: pytest + httpx
- **Frontend**: Manual QA + API Test Scripts
