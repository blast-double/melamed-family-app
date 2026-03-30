"use client";

import { useEffect, useState } from "react";
import { flushSync } from "react-dom";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type {
  MonarchApiResponse,
  MonarchApiSchedule,
  MonarchApiCategory,
  MonarchApiTransaction,
} from "@/lib/types";

const TAX_YEAR = 2025;

const fmt = (n: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    signDisplay: "auto",
  }).format(n);

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger
          onClick={handleCopy}
          className="p-1 rounded hover:bg-zinc-700/50 transition-colors cursor-pointer no-print"
        >
          <span className="text-[10px] font-mono text-zinc-500 hover:text-zinc-300">
            {copied ? "\u2713" : "\u29C9"}
          </span>
        </TooltipTrigger>
        <TooltipContent side="left" className="text-xs">
          {copied ? "Copied!" : "Copy value"}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}

function TransactionRows({ transactions }: { transactions: MonarchApiTransaction[] }) {
  return (
    <>
      {transactions.map((txn) => (
        <TableRow
          key={txn.id}
          className="border-zinc-800/30 hover:bg-zinc-800/20 bg-zinc-950/30 print:bg-white print:border-gray-200"
        >
          <TableCell className="pl-10 text-[11px] font-mono text-zinc-600 print:text-gray-600 print:pl-8">
            <span>{txn.date} &middot; {txn.merchant}</span>
            {txn.plaid_name && txn.plaid_name !== txn.merchant && (
              <span className="block text-[9px] text-zinc-600/60 pl-[72px] print:text-gray-400">
                stmt: {txn.plaid_name}
              </span>
            )}
          </TableCell>
          <TableCell className="text-[11px] font-mono text-zinc-500 truncate max-w-[200px] print:text-gray-500">
            {txn.account}
          </TableCell>
          <TableCell />
          <TableCell className="text-right">
            <span
              className={`text-[11px] font-mono ${
                txn.amount < 0 ? "text-red-400/70 print:text-red-700" : "text-emerald-400/70 print:text-emerald-700"
              }`}
            >
              {fmt(txn.amount)}
            </span>
          </TableCell>
          <TableCell className="w-8 no-print" />
        </TableRow>
      ))}
    </>
  );
}

function CategoryRow({ category, forceExpand }: { category: MonarchApiCategory; forceExpand?: boolean }) {
  const [expanded, setExpanded] = useState(false);
  const isExpanded = expanded || forceExpand;

  return (
    <>
      <TableRow
        className="border-zinc-700/30 hover:bg-zinc-800/20 cursor-pointer print:border-gray-200 print:cursor-default"
        onClick={() => setExpanded(!expanded)}
      >
        <TableCell className="text-xs text-zinc-300 print:text-gray-800 print:font-medium">
          <span className="inline-block w-4 text-zinc-600 mr-1 no-print">
            {isExpanded ? "\u25BE" : "\u25B8"}
          </span>
          {category.name}
        </TableCell>
        <TableCell className="text-[10px] text-zinc-500 italic max-w-[300px] truncate print:text-gray-500">
          {category.note || ""}
        </TableCell>
        <TableCell className="text-xs font-mono text-zinc-500 text-center print:text-gray-600">
          {category.count}
        </TableCell>
        <TableCell className="text-right">
          <span
            className={`font-mono text-sm ${
              category.total < 0 ? "text-red-400 print:text-red-700" : "text-emerald-400 print:text-emerald-700"
            }`}
          >
            {fmt(category.total)}
          </span>
        </TableCell>
        <TableCell className="w-8 no-print" />
      </TableRow>
      {isExpanded && <TransactionRows transactions={category.transactions} />}
    </>
  );
}

function ScheduleFooter({ schedule }: { schedule: MonarchApiSchedule }) {
  const expenseTotal = schedule.categories
    .filter((c) => c.total < 0)
    .reduce((sum, c) => sum + c.total, 0);
  const incomeTotal = schedule.categories
    .filter((c) => c.total > 0)
    .reduce((sum, c) => sum + c.total, 0);
  const hasBoth = expenseTotal < 0 && incomeTotal > 0;

  if (!hasBoth) {
    return (
      <TableRow className="border-zinc-700/30 hover:bg-transparent font-medium print:border-gray-300 print:border-t-2">
        <TableCell className="text-xs text-zinc-200 print:text-gray-900 print:font-bold">NET</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className={`font-mono text-sm font-medium ${schedule.total < 0 ? "text-red-400 print:text-red-700" : "text-emerald-400 print:text-emerald-700"}`}>
            {fmt(schedule.total)}
          </span>
        </TableCell>
        <TableCell className="no-print" />
      </TableRow>
    );
  }

  return (
    <>
      <TableRow className="border-zinc-700/30 hover:bg-transparent print:border-gray-200">
        <TableCell className="text-xs text-zinc-400 print:text-gray-600">EXPENSES</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className="font-mono text-sm text-red-400 print:text-red-700">{fmt(expenseTotal)}</span>
        </TableCell>
        <TableCell className="no-print" />
      </TableRow>
      <TableRow className="border-zinc-700/30 hover:bg-transparent print:border-gray-200">
        <TableCell className="text-xs text-zinc-400 print:text-gray-600">INCOME</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className="font-mono text-sm text-emerald-400 print:text-emerald-700">{fmt(incomeTotal)}</span>
        </TableCell>
        <TableCell className="no-print" />
      </TableRow>
      <TableRow className="border-zinc-700/30 hover:bg-transparent font-medium print:border-gray-300 print:border-t-2">
        <TableCell className="text-xs text-zinc-200 print:text-gray-900 print:font-bold">NET</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className={`font-mono text-sm font-medium ${schedule.total < 0 ? "text-red-400 print:text-red-700" : "text-emerald-400 print:text-emerald-700"}`}>
            {fmt(schedule.total)}
          </span>
        </TableCell>
        <TableCell className="no-print" />
      </TableRow>
    </>
  );
}

function ScheduleSection({ schedule, forceExpand, isFirst }: { schedule: MonarchApiSchedule; forceExpand?: boolean; isFirst?: boolean }) {
  return (
    <section className={isFirst ? "" : "print-page-break"}>
      <div className="flex items-center gap-3 mb-3">
        <h2 className="text-lg font-light text-zinc-200 print:text-gray-900 print:font-semibold">{schedule.display}</h2>
        <div className="flex-1 h-px bg-zinc-800 print:bg-gray-300" />
        <span
          className={`font-mono text-sm ${
            schedule.total < 0 ? "text-red-400 print:text-red-700" : "text-emerald-400 print:text-emerald-700"
          }`}
        >
          {fmt(schedule.total)}
        </span>
      </div>

      <Card className="bg-zinc-900/30 border-zinc-700 overflow-hidden print:bg-white print:border-gray-300">
        <Table>
          <TableHeader>
            <TableRow className="border-zinc-700/30 hover:bg-transparent print:border-gray-200">
              <TableHead className="text-[10px] font-mono text-zinc-600 print:text-gray-500">
                Category
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-600 print:text-gray-500">
                Note to CPA
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-600 text-center print:text-gray-500">
                Count
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-600 text-right print:text-gray-500">
                Total
              </TableHead>
              <TableHead className="w-8 no-print" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {schedule.categories.map((cat) => (
              <CategoryRow key={cat.name} category={cat} forceExpand={forceExpand} />
            ))}
            <ScheduleFooter schedule={schedule} />
          </TableBody>
        </Table>
      </Card>
    </section>
  );
}

function isIncomeOnlySchedule(schedule: MonarchApiSchedule): boolean {
  return schedule.categories.every((c) => c.total >= 0);
}

export default function TriagePage() {
  const [data, setData] = useState<MonarchApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [printMode, setPrintMode] = useState(false);

  useEffect(() => {
    fetch(`/api/monarch?year=${TAX_YEAR}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    const handleBeforePrint = () => {
      flushSync(() => setPrintMode(true));
    };
    const handleAfterPrint = () => {
      setPrintMode(false);
    };
    window.addEventListener("beforeprint", handleBeforePrint);
    window.addEventListener("afterprint", handleAfterPrint);
    return () => {
      window.removeEventListener("beforeprint", handleBeforePrint);
      window.removeEventListener("afterprint", handleAfterPrint);
    };
  }, []);

  const filteredSchedules = data
    ? data.schedules.filter((schedule) => !isIncomeOnlySchedule(schedule))
    : [];

  return (
    <div className="flex-1 flex flex-col">
      {/* Print header — hidden on screen */}
      <div className="hidden print-only print:block print:px-0 print:py-4 print:border-b-2 print:border-gray-900 print:mb-6">
        <h1 className="text-xl font-bold print:text-gray-900">
          Tax Year {TAX_YEAR} — Transaction Detail by Schedule
        </h1>
        <p className="text-sm print:text-gray-500 mt-1">
          Prepared {new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}
          {" "}&middot; Melamed Tax Portal
        </p>
      </div>

      <header className="border-b border-zinc-700 bg-zinc-950/80 backdrop-blur-sm sticky top-0 z-50 no-print">
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="text-xs font-mono text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              &larr; PORTAL
            </Link>
            <div className="h-4 w-px bg-zinc-700" />
            <h1 className="text-sm font-medium text-zinc-200">
              Transaction Verification
            </h1>
            <span className="text-xs font-mono text-zinc-600">{TAX_YEAR}</span>
          </div>

          <div className="flex items-center gap-3">
            {data && (
              <>
                <Badge
                  variant="outline"
                  className="text-[10px] font-mono text-zinc-400 border-zinc-700"
                >
                  {data.total_transactions.toLocaleString()} txns
                </Badge>
                <Badge
                  variant="outline"
                  className="text-[10px] font-mono text-emerald-400 border-emerald-800 bg-emerald-950/30"
                >
                  {data.confidence.high} high
                </Badge>
                <Badge
                  variant="outline"
                  className="text-[10px] font-mono text-amber-400 border-amber-800 bg-amber-950/30"
                >
                  {data.confidence.medium} med
                </Badge>
                {data.needs_review > 0 && (
                  <Badge
                    variant="outline"
                    className="text-[10px] font-mono text-red-400 border-red-800 bg-red-950/30"
                  >
                    {data.needs_review} review
                  </Badge>
                )}
              </>
            )}
            <Button
              size="sm"
              variant="outline"
              className="text-xs border-zinc-700"
              onClick={() => window.print()}
            >
              Print Summary
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-6 space-y-8 print:px-0 print:py-0 print:space-y-6 print:max-w-none">
        {loading && (
          <div className="flex items-center justify-center py-20 no-print">
            <div className="text-center">
              <div className="text-sm text-zinc-400 mb-2">
                Pulling from Monarch Money...
              </div>
              <div className="text-[10px] font-mono text-zinc-600">
                This takes 10-30 seconds
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center py-20 no-print">
            <div className="text-center">
              <div className="text-sm text-red-400 mb-2">Failed to load</div>
              <div className="text-[10px] font-mono text-zinc-600">{error}</div>
            </div>
          </div>
        )}

        {filteredSchedules.map((schedule, idx) => (
          <ScheduleSection
            key={schedule.key}
            schedule={schedule}
            forceExpand={printMode}
            isFirst={idx === 0}
          />
        ))}
      </main>
    </div>
  );
}
