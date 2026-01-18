"use client"

import * as React from "react"
import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { ChatBubble } from "@/components/chat/ChatBubble"
import { ChatInput } from "@/components/chat/ChatInput"
import { api } from "@/services/api"
import { useLanguage } from "@/components/layout/language-context"
import { Sidebar } from "@/components/layout/Sidebar"
import { ProjectDashboard } from "@/components/project/ProjectDashboard"

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
  const [currentSessionId, setCurrentSessionId] = React.useState<number | null>(null)
  const [activeProjectId, setActiveProjectId] = React.useState<string | number | undefined>(undefined)
  const [viewMode, setViewMode] = React.useState<'chat' | 'dashboard'>('chat')

  // Load history from API, but also respect local storage if needed or merge them. 
  // For now, let's use the API for the source of truth if logged in, but the upstream used localStorage.
  // We should prefer the real API history.
  const loadHistory = React.useCallback(async () => {
    try {
      const history = await api.getChatHistory();
      // Map API history to local state structure if they differ, or assume compat
      setChatHistory(history);
    } catch (error) {
      console.error("Failed to load chat history:", error);
    }
  }, []);

  React.useEffect(() => {
    loadHistory();
  }, [loadHistory]);


  // Advanced Chat Handlers (Local state updates for UI, assuming API sync happens or is handled)
  // In a real app we'd call API endpoints here too. For now we update local state to satisfy UI.
  const handlePinChat = (id: number) => {
    setChatHistory(prev => prev.map(chat =>
      chat.id === id ? { ...chat, pinned: !chat.pinned } : chat
    ))
  }

  const handleDeleteChat = async (id: number) => {
    if (confirm("Are you sure you want to delete this chat?")) {
      try {
        await api.deleteChatSession(id);
        setChatHistory(prev => prev.filter(chat => chat.id !== id));
        if (currentSessionId === id) {
          handleNewChat();
        }
      } catch (e: any) {
        console.error("Failed to delete chat", e);
        alert(`Chatni o'chirishda xatolik yuz berdi: ${e.message || "Unknown error"}`);
      }
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

  const handleNewChat = (projectId?: string | number) => {
    setCurrentSessionId(null);
    setActiveProjectId(projectId);
    setMessages([]);
    setIsLoading(false);
    setViewMode('chat');
  };

  const handleProjectClick = (projectId: string | number) => {
    setActiveProjectId(projectId);
    setViewMode('dashboard');
    setCurrentSessionId(null);
    setMessages([]);
  };

  const handleSelectChat = async (sessionId: number) => {
    console.log("DEBUG: handleSelectChat called with sessionId:", sessionId);
    console.log("Selecting chat session:", sessionId);
    setCurrentSessionId(sessionId);
    setViewMode('chat');
    setIsLoading(true);
    try {
      const resp = await api.getChatMessages(sessionId);
      setMessages(resp.map((m: any) => ({
        id: m.message_id.toString(),
        role: m.role,
        content: m.content
      })));
    } catch (e) {
      console.error("Failed to load messages", e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = async (text: string, mode: string, options?: { targetLang?: string, projectId?: string | number, forceNew?: boolean }) => {
    // Determine if it's a feedback action or a real message
    if (mode === 'feedback_positive') {
      alert("Rahmat! (Thanks for your feedback) 👍");
      return;
    }
    if (mode === 'feedback_negative') {
      const reason = prompt("Nima xato ketdi? (What went wrong?)");
      if (reason) {
        alert(`Fikringiz qabul qilindi: "${reason}". \nBiz bu xatoni to'g'irlash ustida ishlaymiz.`);
      }
      return;
    }
    if (mode === 'share') {
      navigator.clipboard.writeText(text);
      alert("Matn nusxalandi va ulashish uchun tayyor! (Copied to clipboard)");
      return;
    }

    if (!text.trim() || isLoading) return;

    // Use forced projectId if provided, otherwise fallback to activeProjectId if we're starting fresh
    const effectiveProjectId = options?.projectId ?? activeProjectId;
    const isActuallyNew = options?.forceNew || currentSessionId === null;
    let sessionIdToUse = isActuallyNew ? null : currentSessionId;

    // Optimistic UI
    const newUserMsg: Message = { id: Date.now().toString(), role: 'user', content: text };
    setMessages((prev) => [...prev, newUserMsg]);
    setIsLoading(true);

    try {
      const context = {
        chatSessionId: sessionIdToUse,
        targetLang: options?.targetLang || language,
        projectId: sessionIdToUse === null ? effectiveProjectId : undefined
      };

      const response = await api.sendMessage(text, mode as any, context);

      if (response.chatSessionId && sessionIdToUse === null) {
        setCurrentSessionId(response.chatSessionId);
        // Refresh history to show new session
        const history = await api.getChatHistory();
        setChatHistory(history);
      }

      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "ai",
        content: response.content,
      }
      setMessages((prev) => [...prev, aiMsg])
    } catch (error) {
      console.error("Failed to send message:", error)
      const errorMsg: Message = {
        id: (Date.now() + 2).toString(),
        role: "ai",
        content: "Sorry, I encountered an error processing your request. Please try again."
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  };

  return (
    <div className="flex min-h-screen w-full bg-transparent font-sans transition-colors duration-300">
      <Sidebar
        history={chatHistory}
        onNewChat={handleNewChat}
        onPinChat={handlePinChat}
        onDeleteChat={handleDeleteChat}
        onRenameChat={handleRenameChat}
        onMoveChat={handleMoveChat}
        onProjectClick={handleProjectClick}
        onSelectChat={handleSelectChat}
      />

      <div className="flex flex-1 flex-col h-screen overflow-hidden">
        <Header />

        <main className="flex flex-1 flex-col items-center p-4 md:p-6 overflow-y-auto">
          {viewMode === 'dashboard' && activeProjectId ? (
            <ProjectDashboard
              project={(() => {
                // Try to find project object from localStorage or state if needed
                // For now, minimal object as required
                const localProjects = JSON.parse(localStorage.getItem("knu_mla_projects") || "[]");
                const found = localProjects.find((p: any) => p.id === activeProjectId);
                return found || { id: activeProjectId, name: "Project", category: "default" };
              })()}
              chats={chatHistory.filter(c => c.projectId === activeProjectId)}
              onNewChat={(text, mode, options) => {
                handleNewChat(activeProjectId);
                handleSend(text, mode, { ...options, projectId: activeProjectId, forceNew: true });
              }}
              onSelectChat={handleSelectChat}
              isLoading={isLoading}
            />
          ) : (
            <div className="flex w-full max-w-3xl flex-1 flex-col">
              {messages.length === 0 ? (
                <div className="flex flex-1 flex-col items-center justify-center text-center space-y-8 py-20 animate-in fade-in slide-in-from-bottom-4 duration-700">
                  <div className="relative group">
                    <img
                      src="/mascot.png"
                      alt="Mascot"
                      className="h-[200px] w-auto object-contain transition-transform duration-500 group-hover:scale-105"
                    />
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
          )}
        </main>

        <div className="w-full bg-transparent p-4 md:px-6 md:pb-6">
          <div className="mx-auto max-w-3xl">
            {viewMode === 'chat' && <ChatInput onSend={handleSend} isLoading={isLoading} />}
            <div className="mt-2 text-center text-xs text-muted-foreground">
              {t.disclaimer}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
