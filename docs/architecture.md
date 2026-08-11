# 🏛️ System Architecture

```
                       +------------------------+
                       |   Next.js Frontend     |
                       | (TypeScript, Tailwind) |
                       +-----------+------------+
                                   | HTTP / REST
                                   v
                       +------------------------+
                       |   FastAPI Backend API  |
                       |  (Main / Routers / DB) |
                       +-----------+------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
+-----------------------+                         +-----------------------+
|  AI Ingestion Engine  |                         |    SQLite Database    |
| - Frame Extractor     |                         | - Tasks & Metadata    |
| - Scene Cut Detector  |                         | - Saved Prompts       |
| - Vision Feature Analyzer                       | - System Options      |
| - Multi-Model Format  |                         +-----------------------+
+-----------------------+
         |
         v
+-----------------------+
|   File Storage Unit   |
| - /uploads            |
| - /frames             |
| - /thumbnails         |
| - /output (TXT/MD/JSON|
+-----------------------+
```

---

## 🔬 AI Engine Pipeline Stages

1. **Ingestion & Validation**: Checks MIME type, container integrity, and extracts stream parameters (FPS, duration, resolution, bit rate).
2. **Frame Sampling**: Extracts uniform temporal keyframes and calculates poster image thumbnails.
3. **Scene Cut Detection**: Compares frame color histograms and SSIM (Structural Similarity Index) across sequential frames to detect cut points and shot transitions.
4. **Vision Feature Analyzer**:
   - **Camera Engine**: Classifies movement (static, panning, tilt, handheld), focal length, shot framing (close-up, wide shot).
   - **Lighting & Color Engine**: Extracts color histograms, primary dominant hex tones, and lighting style (volumetric, neon, soft diffuse).
   - **Objects & Actions Engine**: Identifies focal subjects, context, kinetics, and environment.
5. **Prompt Synthesizer**: Integrates feature vectors into structured prompt text customized for Midjourney v6, Flux.1, SDXL, Sora, and Runway Gen-3.
