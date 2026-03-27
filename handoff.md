# Narrowlitics Handoff — Phase 1 Complete

## What's Done

Narrowlitics is live at **https://captainofindustries.com** with all 4 Docker containers running on Hetzner (178.156.251.26, SSH alias: `filou`).

### Architecture on Hetzner (`/var/www/narrowlitics/`)
- **narrowlitics-frontend**: Next.js 15, port 3020 → proxied through nginx
- **narrowlitics-backend**: FastAPI, port 8005 → proxied at `/api/`
- **narrowlitics-db**: PostgreSQL 16 + pgvector, port 5433
- **narrowlitics-worker**: Celery (stub, ready for Phase 2 tasks)
- **Nginx**: SSL via Let's Encrypt, auto-renewing

### GitHub
Repo: https://github.com/Erstiv/Narrowlitics — all code is there.

### Frontend Pages (all working)
- `/` — Dashboard (shows episode pipeline status, quick stats)
- `/search` — Natural language scene search
- `/tweak` — Tweak Studio placeholder (Phase 4)
- `/admin` — Admin panel (re-index, export, usage stats)

### API Endpoints (all working)
- `GET /api/health` — health check
- `GET /api/episodes/` — list episodes
- `GET /api/episodes/{id}` — get episode
- `PATCH /api/episodes/{id}/status` — update episode status
- `GET /api/scenes/episode/{id}` — list scenes for episode
- `GET /api/scenes/{id}` — get scene
- `POST /api/scenes/episode/{id}/bulk` — bulk ingest Gemini scene data
- `POST /api/search/` — hybrid search (SQL filters now, vector in Phase 2)

### Database
Pre-seeded with The Simpsons show + S04E17 "Last Exit to Springfield" (status: pending).

### Coexisting Services (untouched)
- Cassian: port 8003, planterpruner.com (just fixed SSL today)
- Googloid: port 3000, googloid.com
- SONIX: Docker (internal)
- Plus: lucidnidra (3001), marilynstivers (3002), the-sighs (3003), plinkatron (3005), snap-and-grab (3010), and the full *arr stack

---

## What Elliot Needs Help With Next

### Step 1: Add Gemini API Key to Server

Elliot has the key but needs help adding it to the `.env` file on Hetzner.

The file is at `/var/www/narrowlitics/.env` on the server (SSH alias: `filou`).

The line to update is `GEMINI_API_KEY=` — put the key after the equals sign.

After updating, restart the backend:
```bash
ssh filou "cd /var/www/narrowlitics && docker compose restart narrowlitics-backend narrowlitics-worker"
```

### Step 2: Get the Simpsons Episode to M5 Mac

The episode file lives on Elliot's local Plex server. He needs to:
1. Find the file on Plex (likely an `.mkv` in Plex's media directory)
2. Copy it to somewhere on the M5 Mac (e.g., `~/narrowlitics/input/`)

Plex media is typically stored in a path like `/Volumes/...` or wherever Elliot configured it. He may need help locating the exact file path.

### Step 3: Compress the Episode (on M5 Mac)

The compression script is in the repo. Elliot needs to:

1. Clone the repo on the M5 Mac (if not already):
```bash
git clone https://github.com/Erstiv/Narrowlitics.git ~/narrowlitics
```

2. Make sure FFmpeg is installed:
```bash
brew install ffmpeg
```

3. Run the compression script:
```bash
cd ~/narrowlitics
python3 processing/scripts/compress.py /path/to/simpsons_s04e17.mkv processing/output/compressed.mp4
```

This takes the original file (1-4 GB), shrinks it to 720p at 1 FPS, and outputs a 50-150 MB file optimized for Gemini analysis.

### Step 4: Detect Scene Boundaries (on M5 Mac)

1. Install PySceneDetect:
```bash
pip3 install scenedetect[opencv]
```

2. Run detection on the compressed file:
```bash
python3 processing/scripts/detect_scenes.py processing/output/compressed.mp4 processing/output/scenes.json
```

This outputs a JSON file with start/end timestamps for each scene.

---

## Phase 2 Preview (After Steps 1-4)

Once scenes are detected and the Gemini key is set:
1. Build the Gemini indexing script (upload compressed video, get structured scene JSON)
2. Generate vector embeddings for each scene description
3. Wire up the bulk ingest endpoint to store everything in Postgres
4. Enable real hybrid search (vector similarity + SQL filters)

---

## Important Rules for This Server
- **NEVER kill processes** without being explicitly asked
- Use `systemctl` for service management
- Prefer Python file-write scripts over heredoc blocks (heredocs break with Jinja2)
- Push to GitHub regularly: `github.com/Erstiv/Narrowlitics`
- Elliot is a beginner with server management — explain commands clearly
- Port map: backend=8005, frontend=3020, db=5433
