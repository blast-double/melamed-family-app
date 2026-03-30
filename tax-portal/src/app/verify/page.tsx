"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Separator } from "@/components/ui/separator";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import dynamic from "next/dynamic";

const DocumentDrawer = dynamic(
  () => import("@/components/document-drawer").then((mod) => mod.DocumentDrawer),
  { ssr: false }
);
import { supabase } from "@/lib/supabase";
import type {
  ExtractedDocument,
  ReconciledField,
  ScheduleGroup,
  MonarchApiResponse,
  MonarchApiSchedule,
} from "@/lib/types";
import { CONFIDENCE_COLORS } from "@/lib/types";

const TAX_YEAR = 2025;

// Labels that should never get a $ prefix
const NON_MONETARY_LABELS = [
  /account.*(type|number)/i, /property/i, /address/i, /date/i,
  /origination/i, /number of/i, /state/i, /country/i, /required.*minimum/i,
  /resident/i, /non-covered/i, /type of/i, /basis reported/i,
  /description/i, /cusip/i, /fatca/i,
];

function isMonetaryField(label: string, value: string): boolean {
  if (!value) return false;
  if (NON_MONETARY_LABELS.some((re) => re.test(label))) return false;
  if (/^(yes|no|various|short-term|long-term|gross)$/i.test(value)) return false;
  const cleaned = value.replace(/^-/, "");
  return /^\d+\.\d{2}$/.test(cleaned);
}

// Map document tax_schedule values to Monarch schedule keys
const SCHEDULE_TO_MONARCH_KEY: Record<string, string> = {
  "Schedule E": "schedule_e",
  "Schedule C": "schedule_c",
  "Schedule C — Home Office": "schedule_c_home_office",
  "Schedule B": "reference",
  "Form 1040-ES / 540-ES": "estimated_payments",
};

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

function FieldRow({
  field,
  onVerify,
  verified,
}: {
  field: ReconciledField;
  onVerify: () => void;
  verified: boolean;
}) {
  const colors = CONFIDENCE_COLORS[field.confidence];
  const isZero = field.value === "0.00" || field.value === "0";

  if (isZero) return null;

  return (
    <TableRow className="border-zinc-700/30 hover:bg-zinc-800/20 print:border-gray-200 print:hover:bg-transparent">
      <TableCell className="w-8 no-print">
        <Checkbox checked={verified} onCheckedChange={onVerify} />
      </TableCell>
      <TableCell className="text-xs text-zinc-300 print:text-gray-800">{field.label}</TableCell>
      <TableCell className="text-right">
        <div className="flex items-center justify-end gap-2">
          <span className="font-mono text-sm text-zinc-100 print:text-gray-900">{isMonetaryField(field.label, field.value) ? `$${field.value}` : field.value}</span>
          <CopyButton text={field.value} />
        </div>
      </TableCell>
      <TableCell className="w-28">
        <Badge
          variant="outline"
          className={`text-[10px] font-mono ${colors.text} ${colors.bg} ${colors.border} print:bg-transparent print:text-gray-600 print:border-gray-400`}
        >
          {field.confidence}
        </Badge>
      </TableCell>
      <TableCell className="text-[10px] font-mono text-zinc-400 max-w-[200px] truncate print:text-gray-500">
        {field.schedule_line || "\u2014"}
      </TableCell>
    </TableRow>
  );
}

function DocumentCard({ doc }: { doc: ExtractedDocument }) {
  const [verifiedFields, setVerifiedFields] = useState<Set<string>>(new Set());

  const nonZeroFields = doc.fields.filter(
    (f) => f.value !== "0.00" && f.value !== "0"
  );
  const allVerified =
    nonZeroFields.length > 0 && verifiedFields.size >= nonZeroFields.length;

  const toggleField = (label: string) => {
    setVerifiedFields((prev) => {
      const next = new Set(prev);
      if (next.has(label)) next.delete(label);
      else next.add(label);
      return next;
    });
  };

  const verifyAll = () => {
    setVerifiedFields(new Set(nonZeroFields.map((f) => f.label)));
  };

  const statusColors: Record<string, string> = {
    expected: "text-zinc-500 border-zinc-700",
    received: "text-sky-400 border-sky-800 bg-sky-950/30",
    extracted: "text-emerald-400 border-emerald-800 bg-emerald-950/30",
    submitted: "text-amber-400 border-amber-800 bg-amber-950/30",
    verified: "text-emerald-400 border-emerald-800 bg-emerald-950/30",
  };

  return (
    <Card className="bg-zinc-900/30 border-zinc-700 overflow-hidden print:bg-white print:border-gray-300 print:break-inside-avoid">
      <div className="px-4 py-3 flex items-center justify-between border-b border-zinc-700/50 print:border-gray-200">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-zinc-200 print:text-gray-900">
              {doc.institution}
            </span>
            <Badge variant="outline" className="text-[10px] font-mono text-zinc-500 border-zinc-700 print:text-gray-600 print:border-gray-400">
              {doc.form_type}
            </Badge>
            <Badge
              variant="outline"
              className={`text-[10px] font-mono ${statusColors[doc.status] || statusColors.expected} print:bg-transparent print:text-gray-600 print:border-gray-400`}
            >
              {doc.status}
            </Badge>
          </div>
          {doc.file_path && (
            <div className="text-[10px] font-mono text-zinc-400 mt-0.5 print:text-gray-500">
              {doc.file_path}
            </div>
          )}
        </div>
        <div className="flex items-center gap-2 no-print">
          {doc.file_path && <DocumentDrawer doc={doc} />}
          {nonZeroFields.length > 0 && (
            allVerified ? (
              <Badge className="bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px]">
                Reviewed
              </Badge>
            ) : (
              <Button
                size="sm"
                variant="outline"
                className="text-[10px] h-6 px-2 border-zinc-700"
                onClick={verifyAll}
              >
                Mark All Reviewed
              </Button>
            )
          )}
        </div>
      </div>

      {doc.fields.length > 0 ? (
        <Table>
          <TableHeader>
            <TableRow className="border-zinc-700/30 hover:bg-transparent print:border-gray-200">
              <TableHead className="w-8 no-print" />
              <TableHead className="text-[10px] font-mono text-zinc-400 print:text-gray-500">
                Field
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-400 text-right print:text-gray-500">
                Value
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-400 w-28 print:text-gray-500">
                Confidence
              </TableHead>
              <TableHead className="text-[10px] font-mono text-zinc-400 print:text-gray-500">
                Schedule Line
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {doc.fields.map((field) => (
              <FieldRow
                key={field.label}
                field={field}
                verified={verifiedFields.has(field.label)}
                onVerify={() => toggleField(field.label)}
              />
            ))}
          </TableBody>
        </Table>
      ) : (
        <div className="px-4 py-3 text-[11px] font-mono text-zinc-600 print:text-gray-500">
          No extracted fields yet — run PDF extraction to populate
        </div>
      )}
    </Card>
  );
}

const fmt = (n: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    signDisplay: "auto",
  }).format(n);

function MonarchSummaryCard({
  data,
}: {
  data: ScheduleGroup["monarch_data"];
}) {
  if (!data) return null;

  return (
    <Card className="bg-zinc-900/30 border-zinc-700 overflow-hidden print:bg-white print:border-gray-300 print:break-inside-avoid">
      <div className="px-4 py-3 border-b border-zinc-700/50 print:border-gray-200">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-zinc-200 print:text-gray-900">
            Monarch Money Transactions
          </span>
          <Badge variant="outline" className="text-[10px] font-mono text-zinc-500 border-zinc-700 no-print">
            Live
          </Badge>
        </div>
      </div>
      <Table>
        <TableHeader>
          <TableRow className="border-zinc-700/30 hover:bg-transparent print:border-gray-200">
            <TableHead className="text-[10px] font-mono text-zinc-400 print:text-gray-500">
              Category
            </TableHead>
            <TableHead className="text-[10px] font-mono text-zinc-400 text-center print:text-gray-500">
              Count
            </TableHead>
            <TableHead className="text-[10px] font-mono text-zinc-400 text-right print:text-gray-500">
              Total
            </TableHead>
            <TableHead className="w-8 no-print" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.categories.map((cat) => (
            <TableRow
              key={cat.category}
              className="border-zinc-700/30 hover:bg-zinc-800/20 print:border-gray-200"
            >
              <TableCell className="text-xs text-zinc-300 print:text-gray-800">
                {cat.category}
              </TableCell>
              <TableCell className="text-xs font-mono text-zinc-500 text-center print:text-gray-600">
                {cat.transaction_count}
              </TableCell>
              <TableCell className="text-right">
                <span
                  className={`font-mono text-sm ${
                    cat.total < 0 ? "text-red-400 print:text-red-700" : "text-emerald-400 print:text-emerald-700"
                  }`}
                >
                  {fmt(cat.total)}
                </span>
              </TableCell>
              <TableCell className="no-print">
                <CopyButton text={cat.total.toFixed(2)} />
              </TableCell>
            </TableRow>
          ))}
          <TableRow className="border-zinc-700/30 hover:bg-transparent font-medium print:border-gray-300 print:border-t-2">
            <TableCell className="text-xs text-zinc-200 print:text-gray-900 print:font-bold">Total</TableCell>
            <TableCell />
            <TableCell className="text-right">
              <span
                className={`font-mono text-sm ${
                  data.total < 0 ? "text-red-400 print:text-red-700" : "text-emerald-400 print:text-emerald-700"
                }`}
              >
                {fmt(data.total)}
              </span>
            </TableCell>
            <TableCell className="no-print">
              <CopyButton text={data.total.toFixed(2)} />
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Card>
  );
}

interface SupabaseDoc {
  id: string;
  name: string;
  form_number: string | null;
  tax_schedule: string | null;
  status: string;
  file_path: string | null;
  storage_url: string | null;
  tax_year: number;
  metadata: Record<string, unknown>;
  source_entity: { name: string } | null;
}

function buildScheduleGroups(
  docs: SupabaseDoc[],
  monarchData: MonarchApiResponse | null,
  skipMonarchKeys?: Set<string>
): ScheduleGroup[] {
  // Build Monarch schedule lookup by key
  const monarchByKey = new Map<string, MonarchApiSchedule>();
  if (monarchData) {
    for (const s of monarchData.schedules) {
      monarchByKey.set(s.key, s);
    }
  }

  // Group documents by tax_schedule
  const bySchedule = new Map<string, SupabaseDoc[]>();
  for (const doc of docs) {
    const sched = doc.tax_schedule || "Other";
    if (!bySchedule.has(sched)) bySchedule.set(sched, []);
    bySchedule.get(sched)!.push(doc);
  }

  const groups: ScheduleGroup[] = [];

  for (const [schedule, scheduleDocs] of bySchedule) {
    const display =
      schedule === "Other" ? "Other Documents" : schedule;

    // Convert Supabase docs to ExtractedDocument
    const documents: ExtractedDocument[] = scheduleDocs.map((doc) => {
      // Extract reconciled fields from metadata if present
      const extracted = doc.metadata?.extracted as
        | { fields: ReconciledField[] }
        | undefined;
      const fields: ReconciledField[] = extracted?.fields || [];

      return {
        id: doc.id,
        name: doc.name,
        form_type: doc.form_number || "Unknown",
        institution: doc.source_entity?.name || "Unknown",
        tax_year: doc.tax_year,
        tax_schedule: doc.tax_schedule || "",
        status: doc.status as ExtractedDocument["status"],
        fields,
        file_path: doc.file_path,
        storage_url: doc.storage_url,
      };
    });

    // Find matching Monarch data
    const monarchKey = SCHEDULE_TO_MONARCH_KEY[schedule];
    const monarchSchedule = monarchKey
      ? monarchByKey.get(monarchKey)
      : undefined;

    const monarchSection = monarchSchedule
      ? {
          schedule_key: monarchSchedule.key,
          schedule_display: monarchSchedule.display,
          categories: monarchSchedule.categories.map((c) => ({
            category: c.name,
            transaction_count: c.count,
            total: c.total,
          })),
          total: monarchSchedule.total,
        }
      : null;

    groups.push({
      schedule,
      display,
      documents,
      monarch_data: monarchSection,
    });
  }

  // Add Monarch-only schedules (schedules with transactions but no documents)
  if (monarchData) {
    const docScheduleKeys = new Set(
      Array.from(bySchedule.keys()).map((s) => SCHEDULE_TO_MONARCH_KEY[s])
    );
    for (const ms of monarchData.schedules) {
      if (!docScheduleKeys.has(ms.key) && !skipMonarchKeys?.has(ms.key)) {
        groups.push({
          schedule: ms.display,
          display: ms.display,
          documents: [],
          monarch_data: {
            schedule_key: ms.key,
            schedule_display: ms.display,
            categories: ms.categories.map((c) => ({
              category: c.name,
              transaction_count: c.count,
              total: c.total,
            })),
            total: ms.total,
          },
        });
      }
    }
  }

  return groups;
}

export default function VerifyPage() {
  const [schedules, setSchedules] = useState<ScheduleGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [monarchLoading, setMonarchLoading] = useState(true);

  useEffect(() => {
    let monarchData: MonarchApiResponse | null = null;
    let docs: SupabaseDoc[] = [];

    const fetchDocs = async () => {
      const { data, error: dbError } = await supabase
        .from("documents")
        .select("id, name, form_number, tax_schedule, status, file_path, storage_url, tax_year, metadata, source_entity:entities!source_entity_id(name)")
        .eq("tax_year", TAX_YEAR)
        .neq("status", "expected")
        .order("tax_schedule")
        .order("name");

      if (dbError) throw new Error(dbError.message);
      docs = (data || []) as unknown as SupabaseDoc[];
    };

    const fetchMonarch = async () => {
      try {
        const res = await fetch(`/api/monarch?year=${TAX_YEAR}`);
        if (res.ok) {
          monarchData = await res.json();
        }
      } catch {
        // Monarch data is supplementary — don't block page on failure
      } finally {
        setMonarchLoading(false);
      }
    };

    Promise.all([fetchDocs(), fetchMonarch()])
      .then(() => {
        setSchedules(buildScheduleGroups(docs, monarchData));
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex-1 flex flex-col">
      {/* Print header — hidden on screen */}
      <div className="hidden print:block print:px-0 print:py-4 print:border-b-2 print:border-gray-900 print:mb-6">
        <h1 className="text-xl font-bold print:text-gray-900">
          Tax Year {TAX_YEAR} — Document Verification Summary
        </h1>
        <p className="text-sm print:text-gray-500 mt-1">
          Prepared {new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}
          {" "}&middot; Melamed Tax Portal
        </p>
      </div>

      {/* Header */}
      <header className="border-b border-zinc-700 bg-zinc-950/80 backdrop-blur-sm sticky top-0 z-50 no-print">
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="text-xs font-mono text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              &larr; PORTAL
            </Link>
            <div className="h-4 w-px bg-zinc-800" />
            <h1 className="text-sm font-medium text-zinc-200">
              CPA Verification
            </h1>
            <span className="text-xs font-mono text-zinc-600">{TAX_YEAR}</span>
          </div>
          <div className="flex items-center gap-2">
            {monarchLoading && (
              <Badge variant="outline" className="text-[10px] font-mono text-zinc-500 border-zinc-700">
                Loading Monarch...
              </Badge>
            )}
            <Button
              size="sm"
              variant="outline"
              className="text-xs border-zinc-700"
              onClick={() => window.print()}
            >
              Export Summary
            </Button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-6 space-y-8 print:px-0 print:py-0 print:space-y-6 print:max-w-none">
        {loading && (
          <div className="flex items-center justify-center py-20 no-print">
            <div className="text-sm text-zinc-400">Loading documents...</div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center py-20 no-print">
            <div className="text-center">
              <div className="text-sm text-red-400 mb-2">Failed to load</div>
              <div className="text-[10px] font-mono text-zinc-400">{error}</div>
            </div>
          </div>
        )}

        {!loading && !error && schedules.length === 0 && (
          <div className="flex items-center justify-center py-20 no-print">
            <div className="text-center">
              <div className="text-sm text-zinc-400 mb-2">No documents found</div>
              <div className="text-[10px] font-mono text-zinc-400">
                Seed {TAX_YEAR} documents and mark them as received to populate this view
              </div>
            </div>
          </div>
        )}

        {schedules.map((group, idx) => (
          <section key={group.schedule} className={idx > 0 ? "print-page-break" : ""}>
            <div className="flex items-center gap-3 mb-4">
              <h2 className="text-lg font-light text-zinc-200 print:text-gray-900 print:font-semibold">
                {group.display}
              </h2>
              <div className="flex-1 h-px bg-zinc-800 print:bg-gray-300" />
            </div>

            <div className="space-y-3">
              {group.documents.map((doc) => (
                <DocumentCard key={doc.id} doc={doc} />
              ))}

              {group.monarch_data && (
                <>
                  {group.documents.length > 0 && (
                    <Separator className="bg-zinc-800/50 print:bg-gray-200" />
                  )}
                  <MonarchSummaryCard data={group.monarch_data} />
                </>
              )}
            </div>
          </section>
        ))}
      </main>
    </div>
  );
}
