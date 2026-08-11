"use client";

import Link from "next/link";
import { useHistory } from "@/hooks/useHistory";
import { Film, Trash2, ArrowRight, Clock, Loader2, Sparkles } from "lucide-react";
import { formatSeconds } from "@/lib/utils";

export default function HistoryPage() {
  const { loading, error, historyData, deleteItem } = useHistory();

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">Generation History</h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 font-medium">Review past video prompt generation runs and quick export prompts.</p>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <Loader2 className="h-8 w-8 text-blue-600 dark:text-blue-400 animate-spin" />
        </div>
      ) : error ? (
        <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-6 text-center text-red-600 dark:text-red-400 font-semibold">
          <p>{error}</p>
        </div>
      ) : !historyData || historyData.items.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-12 text-center shadow-sm">
          <Film className="h-12 w-12 text-slate-400 dark:text-slate-600 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-1">No Generation History Yet</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 font-medium">Upload your first video file to start synthesizing prompts.</p>
          <Link
            href="/upload"
            className="inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-700 px-6 py-3 text-sm font-bold text-white shadow-md transition-colors"
          >
            <Sparkles className="h-4 w-4" />
            <span>Upload Video</span>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {historyData.items.map((item: { task_id: string; filename: string; style_preset: string; created_at: string; duration_seconds: number; poster_url: string; prompt_preview: string }) => (
            <div
              key={item.task_id}
              className="group relative flex flex-col justify-between rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 overflow-hidden shadow-sm hover:shadow-md hover:border-blue-600/40 transition-all duration-200"
            >
              <div>
                <div className="relative aspect-video w-full bg-slate-100 dark:bg-slate-950">
                  {item.poster_url ? (
                    <img
                      src={item.poster_url}
                      alt={item.filename}
                      className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  ) : (
                    <div className="flex h-full items-center justify-center text-slate-400 dark:text-slate-600">
                      <Film className="h-8 w-8" />
                    </div>
                  )}
                  <span className="absolute top-3 right-3 rounded-full bg-white/90 dark:bg-slate-900/90 backdrop-blur-md px-2.5 py-1 text-[10px] font-bold text-slate-900 dark:text-white uppercase tracking-wider shadow-xs border border-slate-200 dark:border-slate-800">
                    {item.style_preset}
                  </span>
                </div>

                <div className="p-5 space-y-2">
                  <h3 className="text-base font-bold text-slate-900 dark:text-white truncate">{item.filename}</h3>
                  <div className="flex items-center gap-3 text-xs text-slate-500 dark:text-slate-400 font-medium">
                    <span className="flex items-center gap-1 font-mono">
                      <Clock className="h-3.5 w-3.5" />
                      {formatSeconds(item.duration_seconds)}
                    </span>
                    <span>•</span>
                    <span className="font-mono text-[11px]">{new Date(item.created_at).toLocaleDateString()}</span>
                  </div>

                  <p className="text-xs text-slate-600 dark:text-slate-300 font-mono line-clamp-2 bg-slate-50 dark:bg-slate-950 p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 mt-3">
                    {item.prompt_preview || "Prompt preview generated..."}
                  </p>
                </div>
              </div>

              <div className="flex items-center justify-between border-t border-slate-200 dark:border-slate-800 p-4 bg-slate-50 dark:bg-slate-950/80">
                <button
                  onClick={() => deleteItem(item.task_id)}
                  className="text-xs text-slate-500 dark:text-slate-400 hover:text-red-600 dark:hover:text-red-400 flex items-center gap-1 font-semibold transition-colors"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                  <span>Delete</span>
                </button>

                <Link
                  href={`/result?taskId=${item.task_id}`}
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline"
                >
                  <span>View Details</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
