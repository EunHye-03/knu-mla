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
  const { t } = useLanguage()
  const [messages, setMessages] = React.useState<Message[]>([])
  const [isLoading, setIsLoading] = React.useState(false)

  const handleSend = async (text: string, mode: string) => {
    setIsLoading(true)

    // Add user message
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
    }
    setMessages((prev) => [...prev, userMsg])

    try {
      const response = await api.sendMessage(text, mode);
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "ai",
        content: response.content,
      }
      setMessages((prev) => [...prev, aiMsg])
    } catch (error) {
      console.error("Failed to send message:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen w-full bg-background font-sans transition-colors duration-300">
      <Sidebar />

      <div className="flex flex-1 flex-col h-screen overflow-hidden">
        <Header />

        <main className="flex flex-1 flex-col items-center p-4 md:p-6 overflow-y-auto">
          <div className="flex w-full max-w-3xl flex-1 flex-col">
            {messages.length === 0 ? (
              <div className="flex flex-1 flex-col items-center justify-center text-center space-y-4 py-20">
                <div className="rounded-full bg-red-100 p-4 dark:bg-red-900/20">
                  <div className="text-4xl">👋</div>
                </div>
                <h1 className="text-2xl font-bold tracking-tight">
                  {t.welcome}
                </h1>
                <p className="max-w-[500px] text-muted-foreground">
                  {t.sub_welcome}
                </p>
              </div>
            ) : (
              <div className="flex-1 pb-4">
                {messages.map((msg) => (
                  <ChatBubble
                    key={msg.id}
                    role={msg.role}
                    content={msg.content}
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

        <div className="w-full bg-background p-4 md:px-6 md:pb-6">
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
