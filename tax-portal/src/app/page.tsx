import Link from "next/link";

export default function Home() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="max-w-lg w-full px-6">
        <div className="mb-12">
          <p className="text-xs font-mono text-zinc-500 tracking-widest uppercase mb-2">
            Tax Portal
          </p>
          <h1 className="text-3xl font-light tracking-tight text-zinc-100">
            Melamed — 2025
          </h1>
          <div className="mt-3 h-px bg-gradient-to-r from-zinc-700 to-transparent" />
        </div>

        <div className="space-y-3">
          <Link
            href="/triage"
            className="group block p-5 border border-zinc-700 rounded-lg bg-zinc-900/50 hover:bg-zinc-900 hover:border-zinc-700 transition-all"
          >
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-medium text-zinc-200 group-hover:text-white">
                  Transaction Verification
                </h2>
                <p className="text-xs text-zinc-400 mt-1">
                  Review deductible transactions by schedule with full breakdowns
                </p>
              </div>
              <span className="text-zinc-500 group-hover:text-zinc-300 transition-colors">
                →
              </span>
            </div>
          </Link>

          <Link
            href="/verify"
            className="group block p-5 border border-zinc-700 rounded-lg bg-zinc-900/50 hover:bg-zinc-900 hover:border-zinc-700 transition-all"
          >
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-medium text-zinc-200 group-hover:text-white">
                  CPA Verification
                </h2>
                <p className="text-xs text-zinc-400 mt-1">
                  Review extracted tax form data, verify values, copy to clipboard
                </p>
              </div>
              <span className="text-zinc-500 group-hover:text-zinc-300 transition-colors">
                →
              </span>
            </div>
          </Link>
        </div>

        <p className="mt-8 text-[10px] font-mono text-zinc-500 text-center">
          DUAL-PASS EXTRACTION · GOOGLE OCR + CLAUDE VISION · RECONCILED
        </p>
      </div>
    </div>
  );
}
