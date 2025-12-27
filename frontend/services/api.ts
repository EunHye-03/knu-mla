export interface ChatResponse {
    role: "ai";
    content: string;
}

export const api = {
    sendMessage: async (text: string, mode: string): Promise<ChatResponse> => {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    role: "ai",
                    content: `[${mode.toUpperCase()}] This is a simulated response for: "${text}". The actual AI integration will be implemented in Week 2.`,
                });
            }, 1500);
        });
    },
};
