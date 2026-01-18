import { NextResponse } from 'next/server';

export async function DELETE(request: Request, props: any) {
    const params = await props.params;
    const { id } = params;
    console.log(`[Mock API] Deleting project ${id}`);
    return NextResponse.json({ success: true });
}

export async function PATCH(request: Request, props: any) {
    const params = await props.params;
    const { id } = params;
    console.log(`[Mock API] Updating project ${id}`);
    const body = await request.json();
    return NextResponse.json({ id: id, ...body });
}
