import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as File;

        if (!file) {
            return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
        }

        // Simulation: Just return success and a mock summary
        return NextResponse.json({
            fileId: `file-${Date.now()}`,
            summary: `Analysis complete for ${file.name}. \n\n[MOCK CONTENT]: This document appears to be related to KNU academic guidelines. It covers:\n- Course registration deadlines\n- Visa application procedures\n- Dormitory rules.\n\nThe system has extracted the text and is ready to answer questions about it.`
        });

    } catch (error) {
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
