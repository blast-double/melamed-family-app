"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";

const PDFViewer = dynamic(
  () => import("./pdf-viewer").then((mod) => mod.PDFViewer),
  {
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-full">
        <span className="text-xs font-mono text-zinc-500">Loading viewer...</span>
      </div>
    ),
  }
);
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import type { ExtractedDocument, ReconciledField } from "@/lib/types";
import { CONFIDENCE_COLORS } from "@/lib/types";

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

function CopyBtn({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={async () => {
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 1200);
      }}
      className="p-1 rounded hover:bg-zinc-700/50 transition-colors"
    >
      <span className="text-[10px] font-mono text-zinc-500 hover:text-zinc-300">
        {copied ? "✓" : "⧉"}
      </span>
    </button>
  );
}

function DrawerField({
  field,
  verified,
  onToggle,
}: {
  field: ReconciledField;
  verified: boolean;
  onToggle: () => void;
}) {
  const colors = CONFIDENCE_COLORS[field.confidence];
  const isZero = field.value === "0.00" || field.value === "0";
  if (isZero) return null;

  return (
    <TableRow className="border-zinc-800/30 hover:bg-zinc-800/20">
      <TableCell className="w-8 px-2">
        <Checkbox checked={verified} onCheckedChange={onToggle} />
      </TableCell>
      <TableCell className="text-xs text-zinc-300 py-2">{field.label}</TableCell>
      <TableCell className="text-right py-2">
        <div className="flex items-center justify-end gap-1">
          <span className="font-mono text-sm text-zinc-100">
            {isMonetaryField(field.label, field.value) ? `$${field.value}` : field.value}
          </span>
          <CopyBtn text={field.value} />
        </div>
      </TableCell>
      <TableCell className="w-24 py-2">
        <Badge
          variant="outline"
          className={`text-[10px] font-mono ${colors.text} ${colors.bg} ${colors.border}`}
        >
          {field.confidence}
        </Badge>
      </TableCell>
    </TableRow>
  );
}

export function DocumentDrawer({ doc }: { doc: ExtractedDocument }) {
  const [verifiedFields, setVerifiedFields] = useState<Set<string>>(new Set());

  const nonZeroFields = doc.fields.filter(
    (f) => f.value !== "0.00" && f.value !== "0"
  );

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

  const allVerified =
    nonZeroFields.length > 0 && verifiedFields.size >= nonZeroFields.length;

  const pdfUrl = doc.storage_url || null;

  return (
    <Sheet>
      <SheetTrigger className="inline-flex items-center justify-center rounded-md border border-sky-800 bg-sky-950/30 px-3 h-7 text-xs font-medium text-sky-400 hover:bg-sky-950/50 hover:text-sky-300 transition-colors cursor-pointer">
        View Source Document
      </SheetTrigger>
      <SheetContent
        side="right"
        className="w-[85vw] max-w-[1400px] bg-zinc-950 border-l-2 border-zinc-600 p-0 flex flex-col"
      >
        <SheetHeader className="px-5 py-4 border-b border-zinc-600 shrink-0">
          <SheetTitle className="text-sm font-medium text-zinc-200">
            {doc.institution} — {doc.form_type}
          </SheetTitle>
          <p className="text-[10px] font-mono text-zinc-400">
            {doc.file_path}
          </p>
        </SheetHeader>

        <div className="flex-1 flex min-h-0">
          {/* Left: PDF viewer — takes ~65% */}
          <div className="flex-[2] border-r-2 border-zinc-600 bg-zinc-900/30 min-w-0">
            {pdfUrl ? (
              <PDFViewer url={pdfUrl} />
            ) : (
              <div className="flex items-center justify-center h-full text-zinc-600 text-xs font-mono">
                No PDF available
              </div>
            )}
          </div>

          {/* Right: Extracted fields — takes ~35% */}
          <div className="flex-1 flex flex-col min-w-[280px] max-w-[400px]">
            <div className="px-4 py-3 border-b border-zinc-600 flex items-center justify-between">
              <span className="text-xs font-medium text-zinc-300">
                Extracted Fields
              </span>
              {allVerified ? (
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
              )}
            </div>

            <div className="flex-1 overflow-y-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-zinc-800/30 hover:bg-transparent">
                    <TableHead className="w-8 px-2" />
                    <TableHead className="text-[10px] font-mono text-zinc-400">
                      Field
                    </TableHead>
                    <TableHead className="text-[10px] font-mono text-zinc-400 text-right">
                      Value
                    </TableHead>
                    <TableHead className="text-[10px] font-mono text-zinc-400 w-24">
                      Conf.
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {doc.fields.map((field) => (
                    <DrawerField
                      key={field.label}
                      field={field}
                      verified={verifiedFields.has(field.label)}
                      onToggle={() => toggleField(field.label)}
                    />
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Disputed fields callout */}
            {doc.fields.some((f) => f.confidence === "disputed") && (
              <div className="px-4 py-3 border-t border-amber-900/50 bg-amber-950/20">
                <p className="text-[10px] font-mono text-amber-400">
                  ⚠ Disputed fields detected — compare with PDF
                </p>
                {doc.fields
                  .filter((f) => f.confidence === "disputed")
                  .map((f) => (
                    <div
                      key={f.label}
                      className="mt-1 text-[10px] text-zinc-400"
                    >
                      {f.label}: OCR={f.ocr_value} vs Vision={f.vision_value}
                    </div>
                  ))}
              </div>
            )}
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
