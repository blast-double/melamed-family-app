import { NextRequest } from "next/server";
import { exec } from "child_process";
import path from "path";

const MODAL_ENDPOINT = process.env.MODAL_CATEGORIZE_URL;
const WORKSPACE_ROOT = path.resolve(process.cwd(), "..");

export async function GET(request: NextRequest) {
  const yearParam = request.nextUrl.searchParams.get("year");

  if (!yearParam || !/^\d{4}$/.test(yearParam)) {
    return Response.json({ error: "year parameter required (e.g. ?year=2025)" }, { status: 400 });
  }

  const year = parseInt(yearParam, 10);
  if (year < 2020 || year > 2030) {
    return Response.json({ error: "year out of range" }, { status: 400 });
  }

  try {
    const data = MODAL_ENDPOINT
      ? await fetchFromModal(year)
      : JSON.parse(await runLocal(year));

    return Response.json(data);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("[/api/monarch] Error:", message);
    // Graceful fallback — match MonarchApiResponse contract exactly
    return Response.json({
      tax_year: year,
      total_transactions: 0,
      confidence: { high: 0, medium: 0, low: 0 },
      needs_review: 0,
      schedules: [],
      _note: "Monarch data unavailable — check Modal endpoint or run locally",
    });
  }
}

/** Production: call the Modal web endpoint */
async function fetchFromModal(year: number): Promise<unknown> {
  const url = `${MODAL_ENDPOINT}?year=${year}`;
  const res = await fetch(url, { signal: AbortSignal.timeout(120_000) });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Modal returned ${res.status}: ${text}`);
  }
  return res.json();
}

/** Development: shell out to local Python process */
function runLocal(year: number): Promise<string> {
  return new Promise((resolve, reject) => {
    const venvActivate = process.env.PYTHON_VENV_ACTIVATE || `${process.env.HOME}/venv/bin/activate`;
    const cmd = `source ${venvActivate} && python3 -m execution.finance.categorize --year ${year} --json`;

    exec(cmd, { cwd: WORKSPACE_ROOT, timeout: 120_000, shell: "/bin/zsh" }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`Process exited with code ${error.code}: ${stderr || error.message}`));
        return;
      }
      if (!stdout.trim()) {
        reject(new Error(`Empty output. stderr: ${stderr}`));
        return;
      }
      resolve(stdout.trim());
    });
  });
}
