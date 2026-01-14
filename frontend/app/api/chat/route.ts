import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { text, target_lang, term } = body;

        // Determine mode based on body content or URL if needed, 
        // but for now, we can infer or expect a 'mode' param if we standardized it, 
        // OR we can make separate routes. 
        // The service calls:
        // translate -> { text, target_lang }
        // summarize -> { text }
        // explain -> { term }

        // Let's handle routing based on the specific payload or path.
        // Actually, the plan said one route for chat, but the service calls separate endpoints:
        // /chat/translate, /chat/summarize, /chat/explain.
        // I should probably map them to:
        // app/api/chat/translate/route.ts
        // app/api/chat/summarize/route.ts
        // app/api/chat/explain/route.ts
        // OR use a single route with a query param? 
        // The service does `POST /chat/translate`.
        // So I should create `app/api/chat/translate/route.ts`.

        // Wait, to be cleaner let's stick to the service structure.
        return NextResponse.json({ error: "Use specific endpoints: /api/chat/translate, etc." }, { status: 400 });

    } catch (error) {
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
