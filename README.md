# 🎬 Video-to-Prompt

> Convert any video clip into rich, detailed, multi-style generative AI prompts for **Midjourney v6**, **Flux.1**, **Stable Diffusion XL**, **Runway Gen-3**, **Sora**, and **Pika**.

---

## 🌟 Overview

**Video-to-Prompt** is an end-to-end AI application that breaks down uploaded video files into scene keyframes, performs visual feature analysis (camera tracking, framing, lighting, color palette, subjects, actions, environment, emotional mood), and synthesizes formatted generative text prompts tailored for modern AI image and video models.

---

## 🏗️ Architecture

```text
video-to-prompt/
├── frontend/        # Next.js 14 App Router UI (TypeScript + Tailwind CSS)
├── backend/         # FastAPI Python Server (REST API + SQLite ORM)
├── ai-engine/       # Frame Extractor, Scene Detector, Vision Analyzer, Prompt Engine
├── storage/         # Uploads, Frames, Thumbnails, Scene Cuts, Cache
├── output/          # Exported TXT, JSON, and Markdown Prompts
├── docs/            # Architecture & API specifications
└── docker/          # Dockerfile & Docker-Compose configs
```

---

## 🧠 AI Vision Engine Modes

The Vision Analysis module (`ai-engine/vision/`) operates in two transparent modes:

1. **Computer Vision Heuristic Engine (Fast MVP)**:
   - Uses OpenCV edge detection, color histogram metrics, luminance analysis, and contour spatial positioning for instant keyframe feature extraction.
2. **Local Multimodal Vision AI Model Interface (Pluggable)**:
   - Connects seamlessly to local Vision-LLM models (such as **Qwen2-VL**, **Florence-2**, or **Ollama** `llava` / `qwen2-vl` endpoints) when a local model server is running.

---

## 🔥 Key Features

- **⚡ Multi-Model Prompt Output**: Synthesizes custom prompts for Midjourney v6 (`--ar 16:9 --v 6.0`), Flux.1 Schnell/Dev, SDXL, Sora, and Runway Gen-3.
- **🎥 Scene & Frame Extraction**: Automatic keyframe sampling, poster thumbnail generation, and scene boundary detection via PySceneDetect & OpenCV.
- **👁️ Vision Feature Breakdown**:
  - **Camera Motion**: Static, Pan, Tilt, Dolly Zoom, Tracking Shot, Handheld.
  - **Lighting & Color**: Volumetric light, Golden Hour, Cyberpunk Neon, Teal & Orange palette.
  - **Composition**: Extreme close-up, rule of thirds, anamorphic lens depth.
  - **Actions & Mood**: Subject kinetics, facial expression, emotional mood.
- **🎨 Style Presets**: Standard (Timeline-based) and Creative (Cinematic Breakdown).
- **💾 History & Export**: Save past runs, batch download in TXT/JSON/Markdown, and one-click copy to clipboard.

---

## 🛠️ Quickstart

### Option 1: Docker (Recommended)

```bash
docker-compose -f docker/docker-compose.yml up --build
```

- Frontend UI: `http://localhost:3000`
- Backend API Docs: `http://localhost:8000/docs`

### Option 2: Local Development

#### 1. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📖 Documentation

- [API Specification](docs/api.md)
- [System Architecture](docs/architecture.md)
- [Setup & Deployment Guide](docs/setup.md)
- [Project Roadmap](docs/roadmap.md)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
