"use client"

import * as React from "react"
import { useAuth } from "@/components/auth-provider"

export function BackgroundWrapper() {
    const { user } = useAuth()

    React.useEffect(() => {
        // console.log("BackgroundWrapper user:", user); // Debug
        if (user?.background_image_url) {
            document.body.style.background = 'transparent';
            document.documentElement.style.background = 'transparent';
        } else {
            document.body.style.background = '';
            document.documentElement.style.background = '';
        }
        return () => {
            document.body.style.background = '';
            document.documentElement.style.background = '';
        }
    }, [user?.background_image_url]);

    if (!user?.background_image_url) return null

    return (
        <div
            className="fixed inset-0 z-[-1] bg-cover bg-center bg-no-repeat transition-all duration-500"
            style={{
                backgroundImage: `url(${user.background_image_url})`,
                opacity: 0.6 // Slight transparency to blend with theme? Or full opacity?
                // User wants background. Let's start with full opacity but maybe some overlay in theme?
                // Actually, if it's full opacity, it overrides everything.
                // But the content usually has backgrounds (cards, sidebar).
                // The body background is usually zinc-50.
                // If we put this z-[-1], it sits behind everything.
                // Transparent content will show it.
            }}
        >
            {/* Optional overlay for readability if needed */}
            <div className="absolute inset-0 bg-white/30 dark:bg-black/40 backdrop-blur-[1px]" />
        </div>
    )
}
