
export interface ChatResponse {
    role: "ai" | "user";
    content: string;
    audioUrl?: string; // For potential TTS
    chatSessionId?: number;
}

const API_BASE_URL = '/api';

class ApiService {
    private getToken(): string | null {
        if (typeof window !== 'undefined') {
            return localStorage.getItem('knu_mla_token');
        }
        return null;
    }

    private mapLanguageCode(lang: string): string {
        const normalized = lang.trim().toLowerCase();
        if (['ko', 'kr'].includes(normalized)) return 'ko';
        if (['en'].includes(normalized)) return 'en';
        if (['uz'].includes(normalized)) return 'uz';

        console.warn(`Unexpected language code: "${lang}". Defaulting to 'en'.`);
        return 'en';
    }

    async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
        const url = `${API_BASE_URL}${endpoint}`;
        const token = this.getToken();
        const headers: any = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (token && !headers['Authorization']) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers,
            });

            if (!response.ok) {
                if (response.status === 401) {
                    if (typeof window !== 'undefined') {
                        window.dispatchEvent(new Event('auth-error'));
                    }
                }

                const errorData = await response.json().catch(() => ({}));
                let msg = errorData.detail || errorData.message || `API Error: ${response.statusText}`;
                if (typeof msg === 'object') {
                    // Handle Pydantic validation errors (array of objects)
                    if (Array.isArray(msg) && msg.length > 0 && msg[0].msg) {
                        msg = msg.map((err: any) => err.msg).join('\n');
                    } else {
                        msg = JSON.stringify(msg);
                    }
                }
                throw new Error(msg);
            }

            if (response.status === 204) {
                return {} as T;
            }

            return await response.json();
        } catch (error) {
            console.error(`API Request failed for ${endpoint}:`, error);
            throw error;
        }
    }

    async login(userId: string, password: string): Promise<{ access_token: string, token_type: string }> {
        return this.request<{ access_token: string, token_type: string }>('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, password }),
        });
    }

    async register(data: { user_id: string; nickname: string; password: string; email: string; user_lang: string }): Promise<any> {
        return this.request<any>('/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                ...data,
                user_lang: this.mapLanguageCode(data.user_lang)
            }),
        });
    }

    async getMe(): Promise<any> {
        return this.request<any>('/auth/me', {
            method: 'GET'
        });
    }

    async findId(email: string): Promise<string> {
        return this.request<string>('/auth/find-id', {
            method: 'POST',
            body: JSON.stringify({ email }),
        });
    }

    async resetPassword(userId: string, email: string, newPassword: string): Promise<void> {
        return this.request<void>('/auth/reset-password', {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, email, new_password: newPassword }),
        });
    }

    async deleteAccount(): Promise<void> {
        return this.request<void>('/auth/delete-account', {
            method: 'DELETE',
        });
    }

    async translate(text: string, targetLang: string, chatSessionId?: number): Promise<ChatResponse> {
        const queryString = chatSessionId ? `?chat_session_id=${chatSessionId}` : '';
        const res = await this.request<any>(`/translate${queryString}`, {
            method: 'POST',
            body: JSON.stringify({ text, target_lang: this.mapLanguageCode(targetLang) }),
        });

        return {
            role: 'ai',
            content: res.data?.translated_text || "",
            chatSessionId: res.data?.chat_session_id
        };
    }

    async summarize(text: string, chatSessionId?: number): Promise<ChatResponse> {
        const queryString = chatSessionId ? `?chat_session_id=${chatSessionId}` : '';
        const res = await this.request<any>(`/summarize${queryString}`, {
            method: 'POST',
            body: JSON.stringify({ text }),
        });

        return {
            role: 'ai',
            content: res.data?.summarized_text || "",
            chatSessionId: res.data?.chat_session_id
        };
    }

    async explainTerm(term: string, chatSessionId?: number): Promise<ChatResponse> {
        const queryString = chatSessionId ? `?chat_session_id=${chatSessionId}` : '';
        const res = await this.request<any>(`/term/explain${queryString}`, {
            method: 'POST',
            body: JSON.stringify({ term, target_lang: 'en' }),
        });

        return {
            role: 'ai',
            content: `${res.data?.translated_term}\n\n${res.data?.translated_explanation}` || "",
            chatSessionId: res.data?.chat_session_id
        };
    }

    async chat(message: string, chatSessionId?: number): Promise<ChatResponse> {
        const queryString = chatSessionId ? `?chat_session_id=${chatSessionId}` : '';
        const res = await this.request<any>(`/chat/message${queryString}`, {
            method: 'POST',
            body: JSON.stringify({ message }),
        });

        return {
            role: 'ai',
            content: res.data?.response || "",
            chatSessionId: res.data?.chat_session_id
        };
    }

    async voiceToText(audioBlob: Blob): Promise<{ text: string }> {
        const formData = new FormData();
        formData.append('file', audioBlob, 'voice_message.webm');

        // Note: Content-Type header should NOT be set manually for FormData, fetch handles it
        const url = `${API_BASE_URL}/audio/stt`;
        const token = this.getToken();
        const headers: any = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers
        });

        if (!response.ok) throw new Error('Voice transcription failed');
        return await response.json();
    }

    async uploadFile(file: File): Promise<{ fileId: string; summary?: string }> {
        const formData = new FormData();
        formData.append('file', file);

        const url = `${API_BASE_URL}/files/upload`;
        const token = this.getToken();
        const headers: any = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers
        });

        if (!response.ok) throw new Error('File upload failed');
        return await response.json();
    }

    async updateProfile(data: Partial<{ nickname: string, email: string, user_lang: string, profile_image_url: string, background_image_url: string, is_dark_mode: boolean }>): Promise<any> {
        const payload: any = { ...data };
        if (payload.user_lang) {
            payload.user_lang = this.mapLanguageCode(payload.user_lang);
        }
        return this.request<any>('/users/me', {
            method: 'PATCH',
            body: JSON.stringify(payload),
        });
    }

    // Unified chat method if simpler for the UI to consume
    async sendMessage(text: string, mode: 'translate' | 'summarize' | 'term' | 'chat', context?: any): Promise<ChatResponse> {
        const sessionId = context?.chatSessionId;
        switch (mode) {
            case 'translate':
                return this.translate(text, context?.targetLang || 'en', sessionId);
            case 'summarize':
                return this.summarize(text, sessionId);
            case 'term':
                const termTarget = this.mapLanguageCode(context?.targetLang || 'en');
                const queryString = sessionId ? `?chat_session_id=${sessionId}` : '';
                const res = await this.request<any>(`/term/explain${queryString}`, {
                    method: 'POST',
                    body: JSON.stringify({ term: text, target_lang: termTarget }),
                });
                return {
                    role: 'ai',
                    content: `${res.data?.translated_term}\n\n${res.data?.translated_explanation}` || "",
                    chatSessionId: res.data?.chat_session_id
                };
            case 'chat':
                return this.chat(text, sessionId);
            default:
                throw new Error(`Unsupported mode: ${mode}`);
        }
    }

    async getChatHistory(): Promise<{ id: number, title: string }[]> {
        // Using GET /chat for recent sessions
        const response = await this.request<any>('/chat', {
            method: 'GET'
        });

        if (response.success && response.data && Array.isArray(response.data.results)) {
            return response.data.results.map((item: any) => ({
                id: item.chat_session_id,
                title: item.title
            }));
        }
        return [];
    }
}

export const api = new ApiService();
