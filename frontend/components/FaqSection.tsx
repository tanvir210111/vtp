"use client";

import { useState } from "react";
import { ChevronDown, HelpCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export default function FaqSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const faqs = [
    {
      question: "Supported video formats?",
      answer: "Video-to-Prompt supports standard video containers including MP4 (.mp4), QuickTime MOV (.mov), and WebM (.webm).",
    },
    {
      question: "Maximum video length limit?",
      answer: "The application processes video clips up to 15 seconds long for optimal frame extraction, keyframe density, and speed.",
    },
    {
      question: "What is a Standard Prompt?",
      answer: "A Standard Prompt provides a clean, structured timeline breakdown (0-2s, 2-5s, etc.) focusing on key scenes, subject actions, and direct camera directives.",
    },
    {
      question: "What is a Creative Prompt?",
      answer: "A Creative Prompt generates rich, cinematic descriptive narrative details including atmospheric lighting, volumetric depth, mood parameters, and artistic style tags.",
    },
    {
      question: "Is my video uploaded or stored remotely?",
      answer: "No. All video processing and frame analysis happen locally on your system. Your raw videos remain private and secure.",
    },
  ];

  return (
    <section className="py-16 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0B1120] transition-colors">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 rounded-full border border-purple-600/30 bg-purple-600/10 px-3.5 py-1 text-xs font-bold text-purple-600 dark:text-purple-400 mb-3">
            <HelpCircle className="h-3.5 w-3.5" />
            <span>Got Questions?</span>
          </div>
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight sm:text-4xl">
            Frequently Asked Questions
          </h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Learn more about video format compatibility, prompt styles, and processing limits.
          </p>
        </div>

        <div className="space-y-3.5">
          {faqs.map((faq, index) => {
            const isOpen = openIndex === index;
            return (
              <div
                key={index}
                className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/80 overflow-hidden transition-all shadow-xs"
              >
                <button
                  onClick={() => setOpenIndex(isOpen ? null : index)}
                  className="w-full flex items-center justify-between p-4 sm:p-5 text-left font-bold text-slate-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                >
                  <span className="text-sm sm:text-base">{faq.question}</span>
                  <ChevronDown
                    className={cn(
                      "h-5 w-5 text-slate-500 dark:text-slate-400 transition-transform duration-200 shrink-0",
                      isOpen && "rotate-180 text-blue-600 dark:text-blue-400"
                    )}
                  />
                </button>
                {isOpen && (
                  <div className="px-4 sm:px-5 pb-5 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed border-t border-slate-200 dark:border-slate-800 pt-3 bg-white dark:bg-slate-950/60 font-normal">
                    {faq.answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
