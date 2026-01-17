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
  const [chatHistory, setChatHistory] = React.useState<{ id: number, title: string, pinned?: boolean, projectId?: string | number }[]>([])

  const handleNewChat = () => {
    setMessages([])
    setIsLoading(false)
  }

  // Load history from local storage on mount
  React.useEffect(() => {
    const saved = localStorage.getItem("knu_mla_chat_history")
    if (saved) {
      try {
        setChatHistory(JSON.parse(saved))
      } catch (e) {
        console.error("Failed to parse chat history", e)
      }
    }
  }, [])

  // Save history to local storage whenever it changes
  React.useEffect(() => {
    if (chatHistory.length > 0) {
      localStorage.setItem("knu_mla_chat_history", JSON.stringify(chatHistory))
    }
  }, [chatHistory])

  // Advanced Chat Handlers
  const handlePinChat = (id: number) => {
    setChatHistory(prev => prev.map(chat =>
      chat.id === id ? { ...chat, pinned: !chat.pinned } : chat
    ))
  }

  const handleDeleteChat = (id: number) => {
    if (confirm("Are you sure you want to delete this chat?")) {
      setChatHistory(prev => prev.filter(chat => chat.id !== id))
    }
  }

  const handleRenameChat = (id: number, newTitle: string) => {
    setChatHistory(prev => prev.map(chat =>
      chat.id === id ? { ...chat, title: newTitle } : chat
    ))
  }

  const handleMoveChat = (id: number, projectId: string | number) => {
    setChatHistory(prev => prev.map(chat =>
      chat.id === id ? { ...chat, projectId } : chat
    ))
  }

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

    // If this is the first message, add to history
    if (messages.length === 0) {
      const newHistoryItem = {
        id: Date.now(),
        title: text.length > 30 ? text.substring(0, 30) + "..." : text,
        pinned: false
      }
      setChatHistory(prev => [newHistoryItem, ...prev])
    }

    setMessages((prev) => [...prev, userMsg])

    try {
      // Cast mode to the expected type and pass language context
      const safeMode = (mode === 'translate' || mode === 'summarize' || mode === 'term') ? mode : 'translate';
      // Use selected target language from options, or fallback to current app language
      const targetLang = options?.targetLang || language;
      const response = await api.sendMessage(text, safeMode, { targetLang });

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

  return (
    <div className="flex min-h-screen w-full bg-transparent font-sans transition-colors duration-300">
      <Sidebar
        history={chatHistory}
        onNewChat={handleNewChat}
        onPinChat={handlePinChat}
        onDeleteChat={handleDeleteChat}
        onRenameChat={handleRenameChat}
        onMoveChat={handleMoveChat}
      />

      <div className="flex flex-1 flex-col h-screen overflow-hidden">
        <Header />

        <main className="flex flex-1 flex-col items-center p-4 md:p-6 overflow-y-auto">
          <div className="flex w-full max-w-3xl flex-1 flex-col">
            {messages.length === 0 ? (
              <div className="flex flex-1 flex-col items-center justify-center text-center space-y-8 py-20 animate-in fade-in slide-in-from-bottom-4 duration-700">
                <div className="relative">
                  <div className="absolute inset-0 rounded-full bg-red-100 blur-2xl dark:bg-red-900/20 animate-pulse" />
                  <div className="relative rounded-2xl bg-gradient-to-tr from-red-50 to-white/80 p-6 shadow-xl ring-1 ring-black/5 dark:from-zinc-900/80 dark:to-zinc-800/80 dark:ring-white/10 backdrop-blur-sm">
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
                    <div className="flex items-center gap-3 px-6 py-3 bg-white/80 dark:bg-zinc-800/80 backdrop-blur-md rounded-2xl shadow-xl shadow-red-100/50 dark:shadow-red-900/10 border border-zinc-100 dark:border-zinc-700 animate-in fade-in zoom-in duration-300">
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

        <div className="w-full bg-transparent p-4 md:px-6 md:pb-6">
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
