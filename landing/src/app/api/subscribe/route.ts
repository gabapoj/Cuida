import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { email } = await req.json();

  if (!email || typeof email !== "string") {
    return NextResponse.json({ error: "Invalid email" }, { status: 400 });
  }

  const res = await fetch("https://api.brevo.com/v3/contacts", {
    method: "POST",
    headers: {
      "api-key": process.env.BREVO_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, listIds: [3], updateEnabled: true }),
  });

  if (res.ok || res.status === 204) {
    return NextResponse.json({ ok: true });
  }

  const data = await res.json();
  if (data.code === "duplicate_parameter") {
    return NextResponse.json({ ok: true });
  }

  return NextResponse.json({ error: data.message || "Submission failed" }, { status: 500 });
}
