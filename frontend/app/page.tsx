"use client"

import * as React from "react"
import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { ChatBubble } from "@/components/chat/ChatBubble"
import { ChatInput } from "@/components/chat/ChatInput"
import { api } from "@/services/api"
import { useLanguage } from "@/components/layout/language-context"
import { Sidebar } from "@/components/layout/Sidebar"

type Message = {
  id: string
  role: "user" | "ai"
  content: string
}

export default function Home() {
  const { t, language } = useLanguage()
  const [messages, setMessages] = React.useState<Message[]>([])
  const [isLoading, setIsLoading] = React.useState(false)
  const [chatHistory, setChatHistory] = React.useState<{ id: number, title: string }[]>([])
  const [currentSessionId, setCurrentSessionId] = React.useState<number | null>(null)

  const loadHistory = React.useCallback(async () => {
    try {
      const history = await api.getChatHistory();
      setChatHistory(history);
    } catch (error) {
      console.error("Failed to load chat history:", error);
    }
  }, []);

  React.useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const handleSend = async (text: string, mode: string, options?: { targetLang?: string }) => {
    // Determine if it's a feedback action or a real message
    if (mode === 'feedback_positive') {
      alert("Rahmat! (Thanks for your feedback) 👍");
      return;
    }
    if (mode === 'feedback_negative') {
      const reason = prompt("Nima xato ketdi? (What went wrong?)");
      if (reason) {
        alert(`Fikringiz qabul qilindi: "${reason}". \nBiz bu xatoni to'g'irlash ustida ishlaymiz.`);
        // Here you could technically trigger a regeneration using the feedback
        // For now, we just acknowledge it as per MVP
      }
      return;
    }
    if (mode === 'share') {
      navigator.clipboard.writeText(text);
      alert("Matn nusxalandi va ulashish uchun tayyor! (Copied to clipboard)");
      return;
    }

    setIsLoading(true)

    // Add user message
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
    }

    setMessages((prev) => [...prev, userMsg])

    try {
      // Cast mode to the expected type and pass language context
      const safeMode = (mode === 'translate' || mode === 'summarize' || mode === 'term' || mode === 'chat') ? mode : 'chat';
      // Use selected target language from options, or fallback to current app language
      const targetLang = options?.targetLang || language;

      const response = await api.sendMessage(text, safeMode, {
        targetLang,
        chatSessionId: currentSessionId
      });

      if (response.chatSessionId) {
        const isNewSession = currentSessionId === null;
        setCurrentSessionId(response.chatSessionId);
        if (isNewSession) {
          // Refresh history if we just created a session
          // Small delay to ensure DB write is visible
          setTimeout(() => loadHistory(), 500);
        }
      }

      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "ai",
        content: response.content,
      }
      setMessages((prev) => [...prev, aiMsg])
    } catch (error) {
      console.error("Failed to send message:", error)
      // Optional: Add error message to chat
      const errorMsg: Message = {
        id: (Date.now() + 2).toString(),
        role: "ai",
        content: "Sorry, I encountered an error processing your request. Please try again."
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewChat = () => {
    setCurrentSessionId(null);
    setMessages([]);
  };

  return (
    <div className="flex min-h-screen w-full font-sans transition-colors duration-300">
      <Sidebar history={chatHistory} onNewChat={handleNewChat} />

      <div className="flex flex-1 flex-col h-screen overflow-hidden">
        <Header />

        <main className="flex flex-1 flex-col items-center p-4 md:p-6 overflow-y-auto">
          <div className="flex w-full max-w-3xl flex-1 flex-col">
            {messages.length === 0 ? (
              <div className="flex flex-1 flex-col items-center justify-center text-center space-y-8 py-20 animate-in fade-in slide-in-from-bottom-4 duration-700">
                <div className="relative">
                  <div className="absolute inset-0 rounded-full bg-red-100 blur-2xl dark:bg-red-900/20 animate-pulse" />
                  <div className="relative rounded-2xl bg-gradient-to-tr from-red-50 to-white p-6 shadow-xl ring-1 ring-black/5 dark:from-zinc-900 dark:to-zinc-800 dark:ring-white/10">
                    <div className="text-5xl">👋</div>
                  </div>
                </div>
                <div className="space-y-2 max-w-md">
                  <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-zinc-900 to-zinc-600 bg-clip-text text-transparent dark:from-white dark:to-zinc-400">
                    {t.welcome}
                  </h1>
                  <p className="text-zinc-500 dark:text-zinc-400 leading-relaxed">
                    {t.sub_welcome}
                  </p>
                </div>

                {/* Feature Cards/Suggestions could go here if text allows, keeping it clean for now */}
              </div>
            ) : (
              <div className="flex-1 pb-4">
                {messages.map((msg) => (
                  <ChatBubble
                    key={msg.id}
                    role={msg.role}
                    content={msg.content}
                    onAction={(action, text) => handleSend(text, action)}
                    onCopy={() => {
                      navigator.clipboard.writeText(msg.content)
                      alert("Matn nusxalandi! (Copied to clipboard)")
                    }}
                  />
                ))}
                {isLoading && (
                  <div className="flex w-full justify-center mb-6">
                    {/* Floating 3D Loading Frame */}
                    <div className="flex items-center gap-3 px-6 py-3 bg-white dark:bg-zinc-800 rounded-2xl shadow-xl shadow-red-100/50 dark:shadow-red-900/10 border border-zinc-100 dark:border-zinc-700 animate-in fade-in zoom-in duration-300">
                      <div className="flex space-x-1">
                        <div className="h-2.5 w-2.5 rounded-full bg-red-500 animate-bounce [animation-delay:-0.3s]"></div>
                        <div className="h-2.5 w-2.5 rounded-full bg-red-500 animate-bounce [animation-delay:-0.15s]"></div>
                        <div className="h-2.5 w-2.5 rounded-full bg-red-500 animate-bounce"></div>
                      </div>
                      <span className="text-sm font-medium text-zinc-600 dark:text-zinc-300">{t.analyzing}</span>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </main>

        <div className="w-full p-4 md:px-6 md:pb-6">
          <div className="mx-auto max-w-3xl">
            <ChatInput onSend={handleSend} isLoading={isLoading} />
            <div className="mt-2 text-center text-xs text-muted-foreground">
              {t.disclaimer}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
