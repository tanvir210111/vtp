"use client";

import Link from "next/link";
import {
  Sparkles,
  Video,
  Cpu,
  Github,
  Twitter,
  Terminal,
  ExternalLink,
  Zap,
  Layers,
  Code2,
  Heart,
  ShieldCheck,
  CheckCircle2,
  FileText
} from "lucide-react";

export default function Footer() {
  return (
    <footer className="w-full border-t border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-[#070C18] text-slate-600 dark:text-slate-400 transition-colors pt-16 pb-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-12">
        {/* Main Multi-Column Links Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
          
          {/* Column 1: Brand & Mission (Spans 2 cols on lg) */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 text-white shadow-md shadow-blue-500/20">
                <Sparkles className="h-5 w-5" />
              </div>
              <div>
                <span className="font-extrabold text-slate-900 dark:text-white text-lg tracking-tight">
                  Video to Prompt
                </span>
                <span className="ml-2.5 inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[11px] font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  v1.0.0 Live
                </span>
              </div>
            </div>

            <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed max-w-sm">
              Transform any video clip into production-ready AI prompts using keyframe analysis, camera motion detection, lighting profiling, and multi-model synthesis.
            </p>

            {/* Live Operational Status Banner */}
            <div className="inline-flex items-center gap-2.5 px-3.5 py-2 rounded-xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300 font-medium shadow-xs">
              <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" />
              <span>AI Engine & Vision Pipelines: <strong className="text-emerald-600 dark:text-emerald-400">100% Operational</strong></span>
            </div>

            {/* Social Icons */}
            <div className="flex items-center gap-3 pt-2">
              <a
                href="https://github.com"
                target="_blank"
                rel="noreferrer"
                className="h-9 w-9 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-center text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-white hover:border-blue-500 transition-all shadow-xs"
                aria-label="GitHub Repository"
              >
                <Github className="h-4 w-4" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noreferrer"
                className="h-9 w-9 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-center text-slate-600 dark:text-slate-400 hover:text-blue-500 dark:hover:text-blue-400 hover:border-blue-500 transition-all shadow-xs"
                aria-label="Twitter X"
              >
                <Twitter className="h-4 w-4" />
              </a>
              <a
                href="http://127.0.0.1:8000/docs"
                target="_blank"
                rel="noreferrer"
                className="h-9 w-9 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-center text-slate-600 dark:text-slate-400 hover:text-purple-600 dark:hover:text-purple-400 hover:border-purple-500 transition-all shadow-xs"
                aria-label="API Documentation"
              >
                <Terminal className="h-4 w-4" />
              </a>
            </div>
          </div>

          {/* Column 2: Key Features */}
          <div className="space-y-4">
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-1.5">
              <Zap className="h-3.5 w-3.5 text-blue-500" />
              Features
            </h4>
            <ul className="space-y-2.5 text-xs font-medium">
              <li>
                <Link href="#upload-section" className="hover:text-blue-600 dark:hover:text-white transition-colors flex items-center gap-1.5">
                  <Video className="h-3.5 w-3.5 text-slate-400" />
                  Keyframe Extraction
                </Link>
              </li>
              <li>
                <Link href="#upload-section" className="hover:text-blue-600 dark:hover:text-white transition-colors flex items-center gap-1.5">
                  <Layers className="h-3.5 w-3.5 text-slate-400" />
                  Camera Motion Analysis
                </Link>
              </li>
              <li>
                <Link href="#upload-section" className="hover:text-blue-600 dark:hover:text-white transition-colors flex items-center gap-1.5">
                  <Sparkles className="h-3.5 w-3.5 text-slate-400" />
                  Lighting & Color Profiling
                </Link>
              </li>
              <li>
                <Link href="#upload-section" className="hover:text-blue-600 dark:hover:text-white transition-colors flex items-center gap-1.5">
                  <Code2 className="h-3.5 w-3.5 text-slate-400" />
                  Multi-Model Synthesis
                </Link>
              </li>
              <li>
                <Link href="#history-section" className="hover:text-blue-600 dark:hover:text-white transition-colors flex items-center gap-1.5">
                  <FileText className="h-3.5 w-3.5 text-slate-400" />
                  Prompt History & Export
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: AI Models Supported */}
          <div className="space-y-4">
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-1.5">
              <Cpu className="h-3.5 w-3.5 text-purple-500" />
              Supported Models
            </h4>
            <ul className="space-y-2.5 text-xs font-medium">
              <li className="flex items-center justify-between text-slate-700 dark:text-slate-300">
                <span>Midjourney v6</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 font-mono">v6.0</span>
              </li>
              <li className="flex items-center justify-between text-slate-700 dark:text-slate-300">
                <span>Flux.1 (Dev / Schnell)</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-mono">Dev</span>
              </li>
              <li className="flex items-center justify-between text-slate-700 dark:text-slate-300">
                <span>Stable Diffusion XL</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-600 dark:text-amber-400 font-mono">SDXL</span>
              </li>
              <li className="flex items-center justify-between text-slate-700 dark:text-slate-300">
                <span>OpenAI Sora</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-600 dark:text-purple-400 font-mono">Video</span>
              </li>
              <li className="flex items-center justify-between text-slate-700 dark:text-slate-300">
                <span>Runway Gen-3 Alpha</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 font-mono">Gen-3</span>
              </li>
            </ul>
          </div>

          {/* Column 4: Resources & API */}
          <div className="space-y-4">
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-1.5">
              <Terminal className="h-3.5 w-3.5 text-cyan-500" />
              Resources & API
            </h4>
            <ul className="space-y-2.5 text-xs font-medium">
              <li>
                <a
                  href="http://127.0.0.1:8000/docs"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-blue-600 dark:hover:text-white transition-colors inline-flex items-center gap-1"
                >
                  FastAPI OpenAPI Docs
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
              <li>
                <a
                  href="http://127.0.0.1:8000/api/health"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-blue-600 dark:hover:text-white transition-colors inline-flex items-center gap-1"
                >
                  API Health Status
                  <ExternalLink className="h-3 w-3 text-slate-400" />
                </a>
              </li>
              <li>
                <Link href="#faq-section" className="hover:text-blue-600 dark:hover:text-white transition-colors">
                  Frequently Asked Questions
                </Link>
              </li>
              <li>
                <span className="text-slate-400">Prompt Tuning Guide (v1.0)</span>
              </li>
              <li>
                <span className="text-slate-400">Open Source MIT License</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Tech Stack Banner */}
        <div className="pt-8 border-t border-slate-200 dark:border-slate-800/80 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2 text-xs font-medium text-slate-500 dark:text-slate-400">
            <span>Powered by:</span>
            <span className="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 font-semibold shadow-xs">
              Next.js 14
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 font-semibold shadow-xs">
              FastAPI
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 font-semibold shadow-xs">
              PyTorch & OpenCV
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 font-semibold shadow-xs">
              Gemini Vision AI
            </span>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
            <span>Crafted with</span>
            <Heart className="h-3.5 w-3.5 text-red-500 fill-red-500 inline animate-pulse" />
            <span>for AI Creators & Prompt Engineers</span>
          </div>
        </div>

        {/* Bottom Rights & Links */}
        <div className="pt-6 border-t border-slate-200 dark:border-slate-800/60 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500 dark:text-slate-400 font-medium">
          <div>
            Made by <a href="https://www.linkedin.com/in/tanvir-khan-90122a30" target="_blank" rel="noopener noreferrer" className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 underline">Tanvir Hossain Khan</a>, Software Engineer & SQA Engineer at Media Scope IT, CSE Final Year Student at Daffodil Institute of IT.
          </div>
          <div className="flex items-center gap-6">
            <span className="hover:text-slate-900 dark:hover:text-slate-200 cursor-pointer">Privacy Policy</span>
            <span className="hover:text-slate-900 dark:hover:text-slate-200 cursor-pointer">Terms of Service</span>
            <span className="hover:text-slate-900 dark:hover:text-slate-200 cursor-pointer">Security</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
