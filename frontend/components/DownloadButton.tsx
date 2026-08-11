"use client";

import { useState } from "react";
import { Download, FileText, Code, FileCode } from "lucide-react";
import { getDownloadExportUrl } from "@/lib/api";

interface DownloadButtonProps {
  taskId: string;
}

export default function DownloadButton({ taskId }: DownloadButtonProps) {
  const [isOpen, setIsOpen] = useState(false);

  const formats = [
    { name: "Markdown Report (.md)", format: "markdown", icon: FileText },
    { name: "Raw Prompts Text (.txt)", format: "txt", icon: FileCode },
    { name: "Structured JSON (.json)", format: "json", icon: Code },
  ];

  return (
    <div className="relative inline-block text-left">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center gap-2 rounded-xl bg-surface border border-surface-border px-4 py-2 text-xs font-semibold text-white hover:bg-surface-border transition-colors"
      >
        <Download className="h-4 w-4 text-primary-glow" />
        <span>Export Prompts</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-52 origin-top-right rounded-xl border border-surface-border bg-surface p-1.5 shadow-2xl z-20 backdrop-blur-md">
          {formats.map((item) => {
            const Icon = item.icon;
            return (
              <a
                key={item.format}
                href={getDownloadExportUrl(taskId, item.format)}
                download
                onClick={() => setIsOpen(false)}
                className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-xs text-gray-300 hover:bg-surface-border hover:text-white transition-colors"
              >
                <Icon className="h-4 w-4 text-primary-glow" />
                <span>{item.name}</span>
              </a>
            );
          })}
        </div>
      )}
    </div>
  );
}
