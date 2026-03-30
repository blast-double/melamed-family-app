"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";
import { Button } from "@/components/ui/button";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface PDFViewerProps {
  url: string;
  initialPage?: number;
}

export function PDFViewer({ url, initialPage = 1 }: PDFViewerProps) {
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [containerWidth, setContainerWidth] = useState(600);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        setContainerWidth(entry.contentRect.width);
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (totalPages > 0) {
      setCurrentPage(Math.min(Math.max(1, initialPage), totalPages));
    }
  }, [initialPage, totalPages]);

  const onDocumentLoadSuccess = useCallback(
    ({ numPages }: { numPages: number }) => {
      setTotalPages(numPages);
      setCurrentPage(Math.min(Math.max(1, initialPage), numPages));
    },
    [initialPage]
  );

  return (
    <div ref={containerRef} className="flex flex-col h-full">
      {/* Page controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 py-2 border-b border-zinc-700 bg-zinc-900/80 shrink-0">
          <Button
            size="sm"
            variant="outline"
            className="text-[10px] h-6 px-2 border-zinc-600"
            disabled={currentPage <= 1}
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
          >
            ←
          </Button>
          <span className="text-[10px] font-mono text-zinc-400">
            {currentPage} / {totalPages}
          </span>
          <Button
            size="sm"
            variant="outline"
            className="text-[10px] h-6 px-2 border-zinc-600"
            disabled={currentPage >= totalPages}
            onClick={() =>
              setCurrentPage((p) => Math.min(totalPages, p + 1))
            }
          >
            →
          </Button>
        </div>
      )}

      {/* PDF render area */}
      <div className="flex-1 overflow-auto flex justify-center bg-zinc-900/30 p-2">
        <Document
          file={url}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={
            <div className="flex items-center justify-center h-64">
              <span className="text-xs font-mono text-zinc-500">
                Loading PDF...
              </span>
            </div>
          }
          error={
            <div className="flex items-center justify-center h-64">
              <span className="text-xs font-mono text-red-400">
                Failed to load PDF
              </span>
            </div>
          }
        >
          <Page
            pageNumber={currentPage}
            width={containerWidth - 16}
            renderTextLayer={true}
            renderAnnotationLayer={true}
          />
        </Document>
      </div>
    </div>
  );
}
