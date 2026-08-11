# 📡 Video-to-Prompt REST API Documentation

Base URL: `http://localhost:8000/api`

---

## 🟢 Endpoints

### 1. Health Check
`GET /health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "ai_engine": "ready",
  "storage_status": "writable"
}
```

---

### 2. Upload Video
`POST /upload`

Upload a video file for processing.

**Form Data:**
- `file`: Video binary file (mp4, mov, avi, mkv, webm)

**Response:**
```json
{
  "task_id": "vtp_task_98f4e2a1",
  "filename": "sample_clip.mp4",
  "file_size_bytes": 14258900,
  "duration_seconds": 12.4,
  "resolution": "1920x1080",
  "mime_type": "video/mp4",
  "status": "uploaded"
}
```

---

### 3. Generate Prompt
`POST /generate`

Trigger the AI vision analysis pipeline and prompt generation.

**Request Body:**
```json
{
  "task_id": "vtp_task_98f4e2a1",
  "target_model": "midjourney_v6",
  "style_preset": "cinematic",
  "extract_keyframes": true,
  "scene_threshold": 0.35,
  "custom_negative_prompt": "blurry, low quality, oversaturated"
}
```

**Response:**
```json
{
  "task_id": "vtp_task_98f4e2a1",
  "status": "completed",
  "processing_time_sec": 3.82,
  "analysis": {
    "camera": "Low-angle dynamic tracking shot, cinematic anamorphic lens, 35mm f/1.8",
    "lighting": "Volumetric sunset light with atmospheric golden rim lighting",
    "color_palette": ["#FF8C00", "#1C2833", "#D35400", "#F39C12"],
    "objects": ["cyberpunk skyscraper", "neon reflection", "rain-slicked pavement"],
    "actions": "character walking steadily through futuristic rainy alley",
    "mood": "mysterious, moody, atmospheric"
  },
  "prompts": {
    "midjourney": "Cinematic low-angle tracking shot of a mysterious figure walking through a rainy neon-lit cyberpunk alley at sunset, atmospheric volumetric lighting, anamorphic lens flares, octane render, 8k --ar 16:9 --v 6.0",
    "flux": "A film still, 35mm shot, rainy cyberpunk street reflective wet pavement, dramatic rim lighting, orange and teal mood, ultra detailed texture",
    "sdxl": "A high detail cinematic scene, mysterious character walking in rainy futuristic street, golden hour rim lighting, photorealistic depth of field",
    "runway_gen3": "Dynamic camera tracking shot following character walking forward in rainy cyberpunk city, camera smoothly pans right while keeping focus on subject, natural motion blur",
    "sora": "Continuous cinematic shot moving through a neon-lit wet cyberpunk city street, natural lighting reflections, subtle rain droplet physics on lens"
  },
  "keyframes": [
    "/storage/frames/vtp_task_98f4e2a1/frame_001.jpg",
    "/storage/frames/vtp_task_98f4e2a1/frame_002.jpg"
  ]
}
```

---

### 4. Generation History
`GET /history?page=1&limit=10&style=cinematic`

Query past generated prompt tasks.

**Response:**
```json
{
  "total": 24,
  "page": 1,
  "limit": 10,
  "items": [
    {
      "task_id": "vtp_task_98f4e2a1",
      "filename": "sample_clip.mp4",
      "created_at": "2026-08-06T12:00:00Z",
      "style_preset": "cinematic",
      "prompt_preview": "Cinematic low-angle tracking shot of a mysterious figure...",
      "thumbnail_url": "/storage/thumbnails/vtp_task_98f4e2a1.jpg"
    }
  ]
}
```

---

### 5. Download Export
`GET /download/{task_id}?format=markdown`

Formats: `txt`, `json`, `markdown`.

**Response:** File download stream with formatted prompt analysis report.
