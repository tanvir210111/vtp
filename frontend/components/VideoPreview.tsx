"use client";

import { useState } from "react";
import { Play, Pause, Film, Layers, X } from "lucide-react";

interface VideoPreviewProps {
  file?: File | null;
  videoUrl?: string;
  posterUrl?: string;
  duration?: number;
  onClear?: () => void;
}

export default function VideoPreview({ file, videoUrl, posterUrl, onClear }: VideoPreviewProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const localUrl = file ? URL.createObjectURL(file) : videoUrl;

  if (!localUrl && !posterUrl) return null;

  return (
    <div className="rounded-2xl border border-surface-border bg-surface/40 p-4 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-3 px-1">
        <div className="flex items-center gap-2">
          <Film className="h-4 w-4 text-primary-glow" />
          <span className="text-sm font-semibold text-white">Video Input Preview</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 text-[11px] font-mono text-gray-400 bg-surface px-2.5 py-1 rounded-md border border-surface-border">
            <Layers className="h-3 w-3 text-accent-cyan" />
            <span>Frames Extracted</span>
          </div>
          {onClear && (
            <button
              onClick={onClear}
              type="button"
              className="p-1 rounded-md text-gray-400 hover:text-white hover:bg-slate-800 transition-colors"
              title="Remove video"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      <div className="relative aspect-video w-full overflow-hidden rounded-xl bg-black border border-surface-border">
        {localUrl ? (
          <video
            src={localUrl}
            controls
            poster={posterUrl}
            className="h-full w-full object-contain"
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
          />
        ) : posterUrl ? (
          <img src={posterUrl} alt="Video keyframe poster" className="h-full w-full object-cover" />
        ) : (
          <div className="flex h-full items-center justify-center text-gray-500 text-sm">
            Preview unavailable
          </div>
        )}
      </div>
    </div>
  );
}
