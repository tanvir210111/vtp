"use client";

import Link from "next/link";
import { ArrowRight, Sparkles, Video, Film } from "lucide-react";

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-white dark:bg-[#0B1120] pt-8 pb-16 lg:pt-16 lg:pb-24 border-b border-slate-200 dark:border-slate-800 transition-colors">
      {/* Background radial glow */}
      <div className="absolute top-1/4 left-1/3 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-blue-600/5 dark:bg-blue-600/10 pointer-events-none blur-3xl opacity-70" />

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Side */}
          <div className="lg:col-span-7 text-left space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-blue-600/30 bg-blue-600/10 px-4 py-1.5 text-xs font-bold text-blue-600 dark:text-blue-400 shadow-xs">
              <Sparkles className="h-3.5 w-3.5 text-cyan-600 dark:text-cyan-400" />
              <span>AI Vision Video-to-Prompt v1.0</span>
            </div>

            <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-5xl lg:text-6xl leading-[1.15]">
              Convert Any Video Clip Into{" "}
              <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 dark:from-blue-400 dark:via-purple-400 dark:to-cyan-400 bg-clip-text text-transparent">
                Masterpiece Prompts
              </span>
            </h1>

            <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400 leading-relaxed max-w-2xl font-normal">
              Upload video clips up to 15 seconds. Our local AI vision engine analyzes keyframes, camera movements, lighting, and kinetics to generate precise <strong className="text-slate-900 dark:text-white font-semibold">Standard</strong> and <strong className="text-slate-900 dark:text-white font-semibold">Creative</strong> generative prompts.
            </p>

            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-2">
              <Link
                href="#upload-section"
                className="inline-flex items-center justify-center gap-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white px-7 py-3.5 text-sm font-bold shadow-lg shadow-blue-600/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
              >
                <Video className="h-4 w-4" />
                <span>Upload Video Now</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="/history"
                className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 px-6 py-3.5 text-sm font-semibold text-slate-900 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all duration-200 shadow-xs"
              >
                <Film className="h-4 w-4 text-slate-500 dark:text-slate-400" />
                <span>View History</span>
              </Link>
            </div>

            <div className="pt-4 flex flex-wrap items-center gap-6 text-xs font-medium text-slate-600 dark:text-slate-400">
              <div className="flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
                Max 15 Sec Clips
              </div>
              <div className="flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-full bg-cyan-500"></span>
                Standard & Creative Styles
              </div>
              <div className="flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-full bg-purple-500"></span>
                TXT, JSON, MD Export
              </div>
            </div>
          </div>

          {/* Right Side: Graphic Card Illustration */}
          <div className="lg:col-span-5">
            <div className="relative rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-5 shadow-lg dark:shadow-2xl backdrop-blur-xl group hover:border-blue-500/40 transition-all duration-300">
              <div className="absolute -top-3 -right-3 px-3 py-1 bg-gradient-to-r from-cyan-600 to-blue-600 rounded-full text-[10px] font-bold text-white uppercase tracking-wider shadow-md">
                Interactive AI
              </div>

              <div className="relative aspect-video rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col items-center justify-center p-6 text-center group-hover:scale-[1.01] transition-transform">
                <div className="h-16 w-16 rounded-full bg-blue-600/10 border border-blue-600/20 flex items-center justify-center text-blue-600 dark:text-blue-400 mb-3 shadow-xs">
                  <Film className="h-8 w-8 text-cyan-600 dark:text-cyan-400 animate-pulse" />
                </div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">Drag & Drop Video File</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-xs">Supports MP4, MOV, WEBM (Up to 15 seconds limit)</p>
                <div className="mt-4 flex items-center gap-2 text-[11px] font-mono font-semibold text-cyan-600 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-950/40 px-3 py-1 rounded-md border border-cyan-200 dark:border-cyan-800">
                  <span>AI Vision Frame Analyzer</span>
                </div>
              </div>

              {/* Sample Mini Cards */}
              <div className="mt-4 grid grid-cols-2 gap-3">
                <div className="rounded-lg bg-slate-50 dark:bg-slate-950/60 p-3 border border-slate-200 dark:border-slate-800 text-left shadow-xs">
                  <span className="text-[10px] font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider block">Standard Prompt</span>
                  <p className="text-[11px] text-slate-600 dark:text-slate-400 truncate mt-0.5 font-medium">Structured timeline & camera tags...</p>
                </div>
                <div className="rounded-lg bg-slate-50 dark:bg-slate-950/60 p-3 border border-slate-200 dark:border-slate-800 text-left shadow-xs">
                  <span className="text-[10px] font-bold text-purple-600 dark:text-purple-400 uppercase tracking-wider block">Creative Prompt</span>
                  <p className="text-[11px] text-slate-600 dark:text-slate-400 truncate mt-0.5 font-medium">Cinematic descriptive mood...</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
