export interface MonarchTransaction {
  date: string;
  merchant: string;
  category: string;
  account: string;
  original_statement: string;
  notes: string;
  amount: number;
  tags: string;
  owner: string;
}

export interface AnomalyFlag {
  transaction: MonarchTransaction;
  reason:
    | "uncategorized"
    | "unknown_category"
    | "large_amount"
    | "potential_duplicate"
    | "needs_business_personal_split";
  details: string;
}

export interface TriageDecision {
  transaction_key: string;
  original_category: string;
  resolved_schedule: string;
  is_business: boolean;
  notes: string;
}

export interface TaxSummaryCategory {
  category: string;
  transaction_count: number;
  total: number;
}

export interface TaxSummarySection {
  schedule_key: string;
  schedule_display: string;
  categories: TaxSummaryCategory[];
  total: number;
}

export interface ReconciledField {
  label: string;
  value: string;
  confidence: "verified" | "disputed" | "single_source";
  ocr_value: string | null;
  vision_value: string | null;
  schedule_line: string | null;
}

export interface ExtractedDocument {
  id: string;
  name: string;
  form_type: string;
  institution: string;
  tax_year: number;
  tax_schedule: string;
  status: "expected" | "received" | "extracted" | "verified";
  fields: ReconciledField[];
  file_path: string | null;
}

export type ScheduleGroup = {
  schedule: string;
  display: string;
  documents: ExtractedDocument[];
  monarch_data: TaxSummarySection | null;
};

// --- /api/monarch response types ---

export interface MonarchApiTransaction {
  id: string;
  date: string;
  merchant: string;
  plaid_name?: string;
  amount: number;
  account: string;
  original_name: string;
}

export interface MonarchApiCategory {
  name: string;
  count: number;
  total: number;
  transactions: MonarchApiTransaction[];
  note?: string;
}

export interface MonarchApiSchedule {
  key: string;
  display: string;
  total: number;
  categories: MonarchApiCategory[];
}

export interface MonarchApiResponse {
  tax_year: number;
  total_transactions: number;
  confidence: { high: number; medium: number; low: number };
  needs_review: number;
  schedules: MonarchApiSchedule[];
}

export const SCHEDULE_DISPLAY: Record<string, string> = {
  "Schedule E": "Schedule E — Rental & Passthrough",
  "Schedule D / Form 8949": "Schedule D — Capital Gains & Losses",
  "Schedule D + Schedule B": "Schedule D + B — Investments",
  "Schedule B": "Schedule B — Interest & Dividends",
  "Schedule C": "Schedule C — Business Expenses",
  "Schedule C — Home Office": "Schedule C — Home Office",
  "Form 1040 — Wages": "Form 1040 — Wages",
  "Form 1040-ES / 540-ES": "Estimated Tax Payments",
  "Reference only": "Reference Documents",
};

export const CONFIDENCE_COLORS = {
  verified: { bg: "bg-emerald-950/50", text: "text-emerald-400", border: "border-emerald-800" },
  disputed: { bg: "bg-amber-950/50", text: "text-amber-400", border: "border-amber-800" },
  single_source: { bg: "bg-sky-950/50", text: "text-sky-400", border: "border-sky-800" },
} as const;

export const REASON_LABELS: Record<string, string> = {
  uncategorized: "Uncategorized",
  unknown_category: "Unknown Category",
  large_amount: "Large Amount",
  potential_duplicate: "Potential Duplicate",
  needs_business_personal_split: "Business / Personal",
};
