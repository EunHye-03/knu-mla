# User Flow

## Main Journey
1. **Landing**: User arrives at Chat Interface.
2. **Input**:
   - Types text OR
   - Uploads file (PDF/TXT) OR
   - Records voice.
3. **Action Selection**:
   - Clicks "Translate", "Summarize", or "Explain".
4. **Response**: 
   - AI generates content.
   - User views result in Chat Bubble.

## Edge Cases
- **Network Error**: Show retry toast.
- **Invalid File**: "File type not supported" alert.
- **Empty Input**: Disable send button.
