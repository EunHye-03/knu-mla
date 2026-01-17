import { NextResponse } from 'next/server';

export async function DELETE(request: Request, { params }: { params: { id: string } }) {
    console.log(`[Mock API] Deleting project ${params.id}`);
    return NextResponse.json({ success: true });
}

export async function PATCH(request: Request, { params }: { params: { id: string } }) {
    console.log(`[Mock API] Updating project ${params.id}`);
    const body = await request.json();
    return NextResponse.json({ id: params.id, ...body });
}
