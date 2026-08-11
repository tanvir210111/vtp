"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import PromptCard from "@/components/PromptCard";
import VideoPreview from "@/components/VideoPreview";
import { getTaskStatusApi } from "@/lib/api";
import { ArrowLeft, Clock, Film, Loader2 } from "lucide-react";
import { formatSeconds } from "@/lib/utils";

function ResultContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const taskId = searchParams.get("taskId");

  const [taskData, setTaskData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) {
      setError("No task ID specified.");
      setLoading(false);
      return;
    }

    getTaskStatusApi(taskId)
      .then((data) => {
        setTaskData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to load task details");
        setLoading(false);
      });
  }, [taskId]);

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <Loader2 className="h-10 w-10 text-blue-600 dark:text-blue-400 animate-spin" />
      </div>
    );
  }

  if (error || !taskData) {
    return (
      <div className="mx-auto max-w-xl text-center py-20 px-4">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">Result Not Found</h2>
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">{error || "Task details could not be retrieved."}</p>
        <button
          onClick={() => router.push("/upload")}
          className="rounded-xl bg-blue-600 hover:bg-blue-700 px-6 py-2.5 text-sm font-bold text-white shadow-md transition-colors"
        >
          Return to Upload
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Top Header & Navigation */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <button
            onClick={() => router.push("/upload")}
            className="inline-flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white mb-2 transition-colors font-semibold"
          >
            <ArrowLeft className="h-4 w-4" /> Back to Upload
          </button>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center gap-3">
            Prompt Output
            <span className="text-xs font-mono font-bold text-cyan-600 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-200 dark:border-cyan-800 px-2.5 py-1 rounded-md">
              {taskData.video_id || taskData.task_id}
            </span>
          </h1>
        </div>
      </div>

      {/* Metadata Overview Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-4 backdrop-blur-sm flex items-center gap-3 shadow-xs">
          <Film className="h-5 w-5 text-blue-600 dark:text-blue-400" />
          <div className="min-w-0">
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">File Name</p>
            <p className="text-sm font-bold text-slate-900 dark:text-white truncate">{taskData.filename || "Uploaded Video"}</p>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-4 backdrop-blur-sm flex items-center gap-3 shadow-xs">
          <Clock className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Duration & Resolution</p>
            <p className="text-sm font-bold text-slate-900 dark:text-white">
              {formatSeconds(taskData.duration_seconds || 10.0)} • {taskData.resolution || "1920x1080"}
            </p>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-4 backdrop-blur-sm flex items-center gap-3 shadow-xs">
          <div className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse" />
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Status</p>
            <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400 uppercase">Analysis Completed</p>
          </div>
        </div>
      </div>

      {/* Preview & Prompt Output Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div>
          <VideoPreview posterUrl={taskData.poster_url} />
        </div>
        <div className="lg:col-span-2">
          <PromptCard
            prompts={taskData.prompts || {}}
            analysis={taskData.analysis}
            taskId={taskData.video_id || taskData.task_id}
          />
        </div>
      </div>
    </div>
  );
}

export default function ResultPage() {
  return (
    <Suspense fallback={<div className="p-10 text-center text-slate-500">Loading result page...</div>}>
      <ResultContent />
    </Suspense>
  );
}
