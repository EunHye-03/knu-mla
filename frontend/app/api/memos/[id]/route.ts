import { NextResponse } from 'next/server';

export async function DELETE(request: Request, { params }: { params: { id: string } }) {
    console.log(`[Mock API] Deleting memo ${params.id}`);
    return NextResponse.json({ success: true });
}

export async function PATCH(request: Request, { params }: { params: { id: string } }) {
    console.log(`[Mock API] Updating memo ${params.id}`);
    const body = await request.json();
    return NextResponse.json({ id: params.id, ...body });
}
