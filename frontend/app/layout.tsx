import type { Metadata } from "next";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { ThemeProvider } from "@/components/ThemeProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Video to Prompt Generator | AI Vision Keyframe Synthesizer",
  description: "Extract video keyframes, analyze camera movement, lighting, color palettes, and synthesize prompts for Midjourney v6, Flux.1, SDXL, Sora, and Runway Gen-3.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-white dark:bg-[#0B1120] text-slate-900 dark:text-slate-100 flex flex-col justify-between antialiased selection:bg-blue-500/20">
        <ThemeProvider>
          <div className="flex flex-col min-h-screen justify-between">
            <div>
              <Navbar />
              <main>{children}</main>
            </div>
            <Footer />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
