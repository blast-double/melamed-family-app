import { NextRequest, NextResponse } from "next/server";
import { readFile } from "fs/promises";
import path from "path";

const WORKSPACE_ROOT = path.resolve(process.cwd(), "..");

export async function GET(request: NextRequest) {
  const filePath = request.nextUrl.searchParams.get("path");

  if (!filePath) {
    return NextResponse.json({ error: "path parameter required" }, { status: 400 });
  }

  // Prevent path traversal — must be under tax_document_archive/
  if (!filePath.startsWith("tax_document_archive/") || filePath.includes("..")) {
    return NextResponse.json({ error: "invalid path" }, { status: 403 });
  }

  const fullPath = path.join(WORKSPACE_ROOT, filePath);

  try {
    const fileBuffer = await readFile(fullPath);
    return new NextResponse(fileBuffer, {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `inline; filename="${path.basename(fullPath)}"`,
      },
    });
  } catch {
    return NextResponse.json({ error: "file not found" }, { status: 404 });
  }
}
