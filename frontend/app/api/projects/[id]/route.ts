import { NextResponse } from 'next/server';

export async function DELETE(request: Request, { params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    console.log(`[Mock API] Deleting project ${id}`);
    return NextResponse.json({ success: true });
}

export async function PATCH(request: Request, { params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    console.log(`[Mock API] Updating project ${id}`);
    const body = await request.json();
    return NextResponse.json({ id: id, ...body });
}
