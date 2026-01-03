// ChatResponse interface is defined below
// Actually, earlier it was defined in the file. I will keep it there or improve it.

export interface ChatResponse {
    role: "ai" | "user";
    content: string;
    audioUrl?: string; // For potential TTS
}

const API_BASE_URL = '/api';

class ApiService {
    async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        try {
            const response = await fetch(url, {
                ...options,
                headers,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `API Error: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Request failed for ${endpoint}:`, error);
            throw error;
        }
    }

    async translate(text: string, targetLang: string): Promise<ChatResponse> {
        return this.request<ChatResponse>('/chat/translate', {
            method: 'POST',
            body: JSON.stringify({ text, target_lang: targetLang }),
        });
    }

    async summarize(text: string): Promise<ChatResponse> {
        return this.request<ChatResponse>('/chat/summarize', {
            method: 'POST',
            body: JSON.stringify({ text }),
        });
    }

    async explainTerm(term: string): Promise<ChatResponse> {
        return this.request<ChatResponse>('/chat/explain', {
            method: 'POST',
            body: JSON.stringify({ term }),
        });
    }

    async voiceToText(audioBlob: Blob): Promise<{ text: string }> {
        const formData = new FormData();
        formData.append('file', audioBlob, 'voice_message.webm');

        const response = await fetch(`${API_BASE_URL}/audio/stt`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Voice transcription failed');
        return await response.json();
    }

    async uploadFile(file: File): Promise<{ fileId: string; summary?: string }> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/files/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('File upload failed');
        return await response.json();
    }

    // Unified chat method if simpler for the UI to consume
    async sendMessage(text: string, mode: 'translate' | 'summarize' | 'term', context?: any): Promise<ChatResponse> {
        switch (mode) {
            case 'translate':
                // Defaulting to English or getting from context. 
                // Since context might not be passed purely here, we assume the backend might handle it or we pass a param.
                // ideally, the UI passes the target language.
                return this.translate(text, context?.targetLang || 'en');
            case 'summarize':
                return this.summarize(text);
            case 'term':
                return this.explainTerm(text);
            default:
                throw new Error(`Unsupported mode: ${mode}`);
        }
    }
}

export const api = new ApiService();
