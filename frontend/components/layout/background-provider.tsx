"use client"

import * as React from "react"

export interface BackgroundSettings {
    enabled: boolean
    image: string
    opacity: number
}

interface BackgroundContextType {
    settings: BackgroundSettings
    updateSettings: (settings: Partial<BackgroundSettings>) => void
    availableImages: { id: string, src: string, name: string }[]
}

const defaultSettings: BackgroundSettings = {
    enabled: true,
    image: "/backgrounds/knu-text.png",
    opacity: 0.25
}

const availableImages = [
    { id: "knu-gate", src: "/backgrounds/knu-gate.png", name: "KNU North Gate" },
    { id: "knu-text", src: "/backgrounds/knu-text.png", name: "KNU with Text" },
    { id: "knu-real", src: "/backgrounds/knu-real.png", name: "KNU Campus (Real)" },
]

const BackgroundContext = React.createContext<BackgroundContextType | undefined>(undefined)

export function BackgroundProvider({ children }: { children: React.ReactNode }) {
    const [settings, setSettings] = React.useState<BackgroundSettings>(defaultSettings)
    const [mounted, setMounted] = React.useState(false)

    React.useEffect(() => {
        const stored = localStorage.getItem("knu_mla_bg_settings")
        if (stored) {
            try {
                setSettings(JSON.parse(stored))
            } catch (e) {
                console.error("Failed to parse background settings", e)
            }
        }
        setMounted(true)
    }, [])

    const updateSettings = (newSettings: Partial<BackgroundSettings>) => {
        const updated = { ...settings, ...newSettings }
        setSettings(updated)
        localStorage.setItem("knu_mla_bg_settings", JSON.stringify(updated))
    }


    return (
        <BackgroundContext.Provider value={{ settings, updateSettings, availableImages }}>
            {/* Context Provider */}
            {children}

            {/* Global Background Element */}
            {settings.enabled && (
                <div
                    className="fixed inset-0 z-0 transition-opacity duration-500 pointer-events-none overflow-hidden"
                    style={{ opacity: settings.opacity }}
                >
                    <div
                        className="absolute inset-0 bg-cover bg-center bg-no-repeat transform scale-105 blur-[2px]"
                        style={{ backgroundImage: `url(${settings.image})` }}
                    />
                    {/* Overlay to ensure text readability */}
                    <div className="absolute inset-0 bg-white/40 dark:bg-black/40 mix-blend-overlay" />
                </div>
            )}
        </BackgroundContext.Provider>
    )
}

export function useBackground() {
    const context = React.useContext(BackgroundContext)
    if (context === undefined) {
        throw new Error("useBackground must be used within a BackgroundProvider")
    }
    return context
}
