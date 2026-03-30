"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
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
          className="p-1 rounded hover:bg-zinc-700/50 transition-colors cursor-pointer"
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
          className="border-zinc-800/30 hover:bg-zinc-800/20 bg-zinc-950/30"
        >
          <TableCell className="pl-10 text-[11px] font-mono text-zinc-600">
            <span>{txn.date} &middot; {txn.merchant}</span>
            {txn.plaid_name && txn.plaid_name !== txn.merchant && (
              <span className="block text-[9px] text-zinc-600/60 pl-[72px]">
                stmt: {txn.plaid_name}
              </span>
            )}
          </TableCell>
          <TableCell className="text-[11px] font-mono text-zinc-500 truncate max-w-[200px]">
            {txn.account}
          </TableCell>
          <TableCell />
          <TableCell className="text-right">
            <span
              className={`text-[11px] font-mono ${
                txn.amount < 0 ? "text-red-400/70" : "text-emerald-400/70"
              }`}
            >
              {fmt(txn.amount)}
            </span>
          </TableCell>
          <TableCell className="w-8">
            <CopyButton text={txn.amount.toFixed(2)} />
          </TableCell>
        </TableRow>
      ))}
    </>
  );
}

function CategoryRow({ category }: { category: MonarchApiCategory }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <>
      <TableRow
        className="border-zinc-700/30 hover:bg-zinc-800/20 cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <TableCell className="text-xs text-zinc-300">
          <span className="inline-block w-4 text-zinc-600 mr-1">
            {expanded ? "\u25BE" : "\u25B8"}
          </span>
          {category.name}
        </TableCell>
        <TableCell className="text-[10px] text-zinc-500 italic max-w-[300px] truncate">
          {category.note || ""}
        </TableCell>
        <TableCell className="text-xs font-mono text-zinc-500 text-center">
          {category.count}
        </TableCell>
        <TableCell className="text-right">
          <span
            className={`font-mono text-sm ${
              category.total < 0 ? "text-red-400" : "text-emerald-400"
            }`}
          >
            {fmt(category.total)}
          </span>
        </TableCell>
        <TableCell className="w-8">
          <CopyButton text={category.total.toFixed(2)} />
        </TableCell>
      </TableRow>
      {expanded && <TransactionRows transactions={category.transactions} />}
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
      <TableRow className="border-zinc-700/30 hover:bg-transparent font-medium">
        <TableCell className="text-xs text-zinc-200">NET</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className={`font-mono text-sm font-medium ${schedule.total < 0 ? "text-red-400" : "text-emerald-400"}`}>
            {fmt(schedule.total)}
          </span>
        </TableCell>
        <TableCell><CopyButton text={schedule.total.toFixed(2)} /></TableCell>
      </TableRow>
    );
  }

  return (
    <>
      <TableRow className="border-zinc-700/30 hover:bg-transparent">
        <TableCell className="text-xs text-zinc-400">EXPENSES</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className="font-mono text-sm text-red-400">{fmt(expenseTotal)}</span>
        </TableCell>
        <TableCell><CopyButton text={expenseTotal.toFixed(2)} /></TableCell>
      </TableRow>
      <TableRow className="border-zinc-700/30 hover:bg-transparent">
        <TableCell className="text-xs text-zinc-400">INCOME</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className="font-mono text-sm text-emerald-400">{fmt(incomeTotal)}</span>
        </TableCell>
        <TableCell><CopyButton text={incomeTotal.toFixed(2)} /></TableCell>
      </TableRow>
      <TableRow className="border-zinc-700/30 hover:bg-transparent font-medium">
        <TableCell className="text-xs text-zinc-200">NET</TableCell>
        <TableCell />
        <TableCell />
        <TableCell className="text-right">
          <span className={`font-mono text-sm font-medium ${schedule.total < 0 ? "text-red-400" : "text-emerald-400"}`}>
            {fmt(schedule.total)}
          </span>
        </TableCell>
        <TableCell><CopyButton text={schedule.total.toFixed(2)} /></TableCell>
      </TableRow>
    </>
  );
}

function ScheduleSection({ schedule }: { schedule: MonarchApiSchedule }) {
  return (
    <section>
      <div className="flex items-center gap-3 mb-3">
        <h2 className="text-lg font-light text-zinc-200">{schedule.display}</h2>
        <div className="flex-1 h-px bg-zinc-800" />
        <span
          className={`font-mono text-sm ${
            schedule.total < 0 ? "text-red-400" : "text-emerald-400"
          }`}
        >
          {fmt(schedule.total)}
        </span>
      </div>

      <Card className="bg-zinc-900/30 border-zinc-700 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="border-zinc-700/30 hover:bg-transparent">
              <TableHead className="text-[10px] font-mono text-zinc-600">
                Category
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-600">
                Note to CPA
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-600 text-center">
                Count
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-600 text-right">
                Total
              </TableHead>
              <TableHead className="w-8" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {schedule.categories.map((cat) => (
              <CategoryRow key={cat.name} category={cat} />
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

  return (
    <div className="flex-1 flex flex-col">
      <header className="border-b border-zinc-700 bg-zinc-950/80 backdrop-blur-sm sticky top-0 z-50">
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

          {data && (
            <div className="flex items-center gap-3">
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
            </div>
          )}
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-6 space-y-8">
        {loading && (
          <div className="flex items-center justify-center py-20">
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
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="text-sm text-red-400 mb-2">Failed to load</div>
              <div className="text-[10px] font-mono text-zinc-600">{error}</div>
            </div>
          </div>
        )}

        {data &&
          data.schedules
            .filter((schedule) => !isIncomeOnlySchedule(schedule))
            .map((schedule) => (
              <ScheduleSection key={schedule.key} schedule={schedule} />
            ))}
      </main>
    </div>
  );
}
