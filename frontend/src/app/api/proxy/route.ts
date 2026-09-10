import type { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const path = searchParams.get("path") || "";
  const res = await fetch(
    `${process.env.BACKEND_URL || "http://localhost:8000"}/api/v1/${path}`,
    { cache: "no-store" }
  );
  const data = await res.json();
  return Response.json(data, { status: res.status });
}