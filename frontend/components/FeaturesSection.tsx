"use client";

import { Eye, Sparkles, Wand2, Download, History } from "lucide-react";

export default function FeaturesSection() {
  const features = [
    {
      icon: Eye,
      color: "text-blue-600 dark:text-blue-400 bg-blue-600/10 border-blue-600/20",
      title: "AI Video Analysis",
      description: "Automated keyframe sampling, scene boundary detection, camera movement tracking, lighting & color tone breakdown.",
    },
    {
      icon: Sparkles,
      color: "text-purple-600 dark:text-purple-400 bg-purple-600/10 border-purple-600/20",
      title: "Standard Prompt",
      description: "Timeline-based (0-2s, 2-5s) clean structured prompts optimized for exact scene reproduction.",
    },
    {
      icon: Wand2,
      color: "text-cyan-600 dark:text-cyan-400 bg-cyan-600/10 border-cyan-600/20",
      title: "Creative Prompt",
      description: "Rich cinematic descriptions detailing atmospheric lighting, depth of field, kinetics, and artistic mood.",
    },
    {
      icon: Download,
      color: "text-emerald-600 dark:text-emerald-400 bg-emerald-600/10 border-emerald-600/20",
      title: "Multi-Format Export",
      description: "One-click copy to clipboard and downloadable formatted prompt reports in TXT, JSON, and Markdown.",
    },
    {
      icon: History,
      color: "text-amber-600 dark:text-amber-400 bg-amber-600/10 border-amber-600/20",
      title: "Prompt History",
      description: "Local history storage allowing you to search, review, and re-export past video generation prompts anytime.",
    },
  ];

  return (
    <section className="py-16 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#0B1120]/50 transition-colors">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight sm:text-4xl">
            Everything You Need For <span className="text-blue-600 dark:text-blue-400">Generative Video AI</span>
          </h2>
          <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">
            Powered by local frame processing & vision models to transform raw clips into tailored prompt masterworks.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => {
            const Icon = feature.icon;
            return (
              <div
                key={i}
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-6 shadow-sm hover:shadow-md hover:border-slate-300 dark:hover:border-slate-700 transition-all duration-200 group"
              >
                <div className={`h-12 w-12 rounded-xl border flex items-center justify-center mb-4 transition-transform group-hover:scale-105 ${feature.color}`}>
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">{feature.title}</h3>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 leading-relaxed font-normal">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
