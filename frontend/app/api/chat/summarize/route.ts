import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const { text } = await request.json();

        // Simulation Logic
        // Simulation Logic
        const content = {
            summary: `Here is a concise summary of the provided text. The content has been processed to highlight key points regarding "${text.substring(0, 20)}...". This text explains the core concepts and provides a brief overview of the subject matter.`,
            key_points: [
                "The text discusses the importance of the subject.",
                "It highlights three main arguments supporting the thesis.",
                "The conclusion suggests further research is needed."
            ],
            keywords: ["summary", "analysis", "key points", "education"]
        };

        return NextResponse.json({
            role: "ai",
            content: JSON.stringify(content)
        });

    } catch (error) {
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
