"""
General chat service for ChatGPT-like conversations
"""
from app.services.openai_service import call_llm, OpenAIRateLimitError, OpenAIUpstreamError
from app.exceptions.error import AppError, ErrorCode


def general_chat(message: str) -> str:
    """
    General chat function for free-form conversation with AI
    
    Args:
        message: User's message
        
    Returns:
        AI's response
        
    Raises:
        OpenAIRateLimitError: If rate limit exceeded
        OpenAIUpstreamError: If OpenAI API error
        AppError: For other errors
    """
    
    system_prompt = """You are a helpful AI assistant for KNU (Kyungnam University) students.
You can help with:
- Answering questions about university life
- Explaining academic concepts  
- Providing study tips
- General conversation
- Translation and language help
- Summarizing information

Be friendly, helpful, and concise. Respond in the same language as the user's question."""

    try:
        response = call_llm(
            system_prompt=system_prompt,
            user_prompt=message,
            model="gpt-4o-mini",
            temperature=0.7,  # More creative for general chat
            max_tokens=1000   # Longer responses for chat
        )
        
        return response
        
    except OpenAIRateLimitError:
        raise
    except OpenAIUpstreamError:
        raise
    except Exception as e:
        raise AppError(
            error_code=ErrorCode.INTERNAL_ERROR,
            message=f"Failed to generate chat response: {str(e)}",
            status_code=500
        )
