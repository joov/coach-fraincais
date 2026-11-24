# Coach Français – Architektur

## Übersicht

Das System besteht aus drei Docker-Containern, orchestriert über Docker Compose:

```
┌─────────────────────────────────────────────────────────────────┐
│  Docker Compose                                                 │
│                                                                 │
│  ┌──────────────┐   ┌──────────────────┐   ┌────────────────┐  │
│  │   Frontend    │   │     Backend      │   │    Whisper      │  │
│  │              │   │                  │   │                │  │
│  │  Vue.js SPA  │──▶│  FastAPI (Python) │──▶│  Faster-Whisper │  │
│  │  + TTS       │   │  + SQLite        │   │  REST API       │  │
│  │  (Browser)   │◀──│  + LLM-Client    │◀──│  (CPU, base)    │  │
│  │              │   │                  │   │                │  │
│  │  :5173       │   │  :8000           │   │  :9000         │  │
│  └──────────────┘   └───────┬──────────┘   └────────────────┘  │
│                             │                                   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼ (HTTPS)
                    ┌──────────────────┐
                    │  LLM Provider    │
                    │  (OpenAI-kompa-  │
                    │   tible API)     │
                    │                  │
                    │  z.B. OpenCode   │
                    │  Zen, OpenAI,    │
                    │  Anthropic, ...  │
                    └──────────────────┘
```

### Designprinzipien

- **Sprache bleibt lokal:** TTS läuft im Browser (Web Speech API), STT läuft im Whisper-Container. Audiodaten verlassen nicht das lokale Netzwerk.
- **Nur der Trainingsplan ist extern:** Lektionen, Übungen und Feedback laufen über Ollama auf dem Host (`OLLAMA_MODEL`, aktuell `gemma4`).
- **Einzelnutzer-Betrieb:** Kein Auth, kein Multi-Tenancy. Lokales System für einen Lernenden.
- **Vollständig containerisiert:** Ein einziges `docker compose up` startet das gesamte System.

---

## Container 1: Frontend (Vue.js)

### Aufgabe
- Benutzeroberfläche für Navigation, Lektionsansicht und Übungen
- **Text-to-Speech (TTS)** direkt im Browser
- **Audio-Aufnahme** über das Mikrofon des Nutzers

### Technologie-Stack
| Komponente | Technologie |
|---|---|
| Framework | Vue.js 3 (Composition API) |
| Build-Tool | Vite |
| Styling | Tailwind CSS oder vergleichbar |
| TTS | Web Speech API (`SpeechSynthesis`) |
| Audio-Aufnahme | MediaRecorder API |
| HTTP-Client | Axios oder fetch |
| Serving (Prod) | nginx |

### TTS im Browser (Text-to-Speech)

Die Sprachausgabe nutzt die **Web Speech API**, die in allen modernen Browsern verfügbar ist:

```javascript
const utterance = new SpeechSynthesisUtterance("Bonjour, comment allez-vous ?");
utterance.lang = "fr-FR";
utterance.rate = 0.85; // Langsamer für Anfänger
speechSynthesis.speak(utterance);
```

- Sprache: `fr-FR` (französisch, Frankreich)
- Geschwindigkeit: Konfigurierbar (0.5 = langsam, 1.0 = normal)
- Stimme: Die beste verfügbare französische Stimme wird automatisch gewählt
- **Keine externen API-Aufrufe** – die Synthese erfolgt vollständig im Browser

### Audio-Aufnahme (Mikrofon)

Die Aufnahme des Nutzers erfolgt über die **MediaRecorder API**:

```javascript
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
const recorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });
```

- Format: WebM/Opus (kompakt, von Whisper unterstützt)
- Die Aufnahme wird nach dem Stoppen als Blob an das Backend gesendet
- Das Frontend zeigt einen visuellen Aufnahme-Indikator (Waveform oder Pegelanzeige)

### Kommunikation mit dem Backend

Alle Interaktionen laufen über REST-Aufrufe an das Backend:

| Endpunkt | Methode | Beschreibung |
|---|---|---|
| `/api/plan` | POST | Trainingsplan generieren |
| `/api/plan` | GET | Aktuellen Trainingsplan abrufen |
| `/api/lessons/{id}` | GET | Lektionsinhalte abrufen |
| `/api/exercises/{id}` | GET | Übungen einer Lektion abrufen |
| `/api/exercises/{id}/answer` | POST | Antwort auf Übung einreichen |
| `/api/speech/transcribe` | POST | Audio zur Transkription senden |
| `/api/progress` | GET | Fortschritt und Fehleranalyse abrufen |
| `/api/progress/level` | GET | Niveau-Einschätzung abrufen |
| `/api/settings` | GET/PUT | Benutzereinstellungen |

### Docker-Konfiguration

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5173
```

Der nginx leitet API-Aufrufe (`/api/*`) per Reverse Proxy an den Backend-Container weiter.

---

## Container 2: Backend (FastAPI + SQLite)

### Aufgabe
- REST-API für Frontend
- Geschäftslogik (Trainingsplan, Übungssteuerung, Fortschrittstracking)
- Kommunikation mit dem LLM (Trainingsplan-Generierung, Übungsinhalte)
- Weiterleitung von Audio an den Whisper-Container
- Persistenz (SQLite)

### Technologie-Stack

| Komponente | Technologie |
|---|---|
| Framework | FastAPI |
| Python-Version | 3.12+ |
| ORM | SQLAlchemy / SQLModel |
| Datenbank | SQLite (Datei im Volume) |
| LLM-Client | openai Python SDK (OpenAI-kompatible API) |
| HTTP-Client (intern) | httpx (async, für Whisper-Aufrufe) |
| Migrations | Alembic |

### LLM-Anbindung (Trainingsplan & Übungserstellung)

Die Kommunikation mit dem LLM erfolgt über das **OpenAI Python SDK** mit konfigurierbarem Endpunkt und Modell. Dadurch kann jedes Modell verwendet werden, das eine OpenAI-kompatible API bereitstellt – einschließlich der Modelle aus der OpenCode-Zen-Plattform.

#### Konfiguration per Umgebungsvariablen

```env
# .env
LLM_API_BASE_URL=https://opencode.ai/inference/openai/v1  # OpenCode Console
LLM_API_KEY=sk-...                               # API-Key
LLM_MODEL=claude-sonnet-5-5                      # Modell-ID ohne Provider-Prefix
LLM_TEMPERATURE=0.7                              # Kreativität
LLM_MAX_TOKENS=4096                              # Max. Antwortlänge
```

#### Verwendung im Code

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url=settings.llm_api_base_url,
    api_key=settings.llm_api_key,
)

response = await client.chat.completions.create(
    model=settings.llm_model,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT_TRAININGSPLAN},
        {"role": "user", "content": user_request},
    ],
    temperature=settings.llm_temperature,
    max_tokens=settings.llm_max_tokens,
)
```

#### Einsatzbereiche des LLMs

| Funktion | Beschreibung |
|---|---|
| Trainingsplan generieren | Aus Zielniveau, Schwerpunkten, Themen und Zeitbudget einen individuellen Plan erstellen |
| Lektionsinhalte erstellen | Dialoge (formell + informell) für jede Lektion generieren |
| Übungen erstellen | Lückentexte, Multiple-Choice, Sätze ordnen etc. passend zum Lektionsthema |
| Grammatik-Box | Zusammenfassung der Grammatikregeln pro Lektion |
| Fehleranalyse | Fehlermuster erkennen und Empfehlungen formulieren |
| Niveau-Einschätzung | Basierend auf Übungsergebnissen das aktuelle Niveau bewerten |
| Aussprache-Feedback | Transkription mit Zieltext vergleichen und Korrekturen formulieren |

#### Modellwechsel zur Laufzeit

Das Modell kann über den Einstellungs-Endpunkt (`PUT /api/settings`) auch zur Laufzeit gewechselt werden, ohne den Container neu zu starten. So kann der Nutzer z.B. zwischen verschiedenen OpenCode-Zen-Modellen hin- und herwechseln.

### Datenbankschema (SQLite)

```
┌──────────────────┐     ┌──────────────────────┐
│     user          │     │   training_plan      │
├──────────────────┤     ├──────────────────────┤
│ id (PK)          │     │ id (PK)              │
│ name             │     │ user_id (FK)         │
│ current_level    │     │ target_level         │
│ target_level     │     │ grammar_focus (JSON) │
│ created_at       │     │ topic_focus (JSON)   │
│ settings (JSON)  │     │ time_budget (JSON)   │
└────────┬─────────┘     │ plan_data (JSON)     │
         │               │ created_at           │
         │               └──────────┬───────────┘
         │                          │
         ▼                          ▼
┌──────────────────┐     ┌──────────────────────┐
│   lesson          │     │  plan_lesson         │
├──────────────────┤     ├──────────────────────┤
│ id (PK)          │     │ id (PK)              │
│ number           │     │ plan_id (FK)         │
│ title            │     │ lesson_id (FK)       │
│ topic            │     │ order_index          │
│ grammar_focus    │     │ status (enum)        │
│ level            │     │ scheduled_date       │
│ block            │     └──────────────────────┘
│ dialogues (JSON) │
│ exercises (JSON) │
│ grammar_box(JSON)│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────────┐
│  exercise_result  │     │   error_log          │
├──────────────────┤     ├──────────────────────┤
│ id (PK)          │     │ id (PK)              │
│ user_id (FK)     │     │ user_id (FK)         │
│ lesson_id (FK)   │     │ lesson_id (FK)       │
│ exercise_type    │     │ exercise_type        │
│ register (enum)  │     │ error_category       │
│ user_answer      │     │ error_detail         │
│ correct_answer   │     │ register (enum)      │
│ is_correct       │     │ created_at           │
│ attempt_number   │     └──────────────────────┘
│ created_at       │
└──────────────────┘

enum register: "formal" | "informal"
enum status: "pending" | "in_progress" | "completed" | "skipped"
```

### Docker-Konfiguration

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Das SQLite-Datenbankfile wird in ein Docker Volume gemountet, damit Daten zwischen Container-Neustarts erhalten bleiben.

---

## Container 3: Whisper (Faster-Whisper STT)

### Aufgabe
- Speech-to-Text: Audioaufnahmen des Nutzers in Text umwandeln
- Läuft lokal auf CPU – Audiodaten verlassen den Rechner nicht

### Technologie-Stack

| Komponente | Technologie |
|---|---|
| STT-Engine | Faster-Whisper |
| Modell | `base` (Default, konfigurierbar) |
| Compute | CPU (ct2 int8-Quantisierung) |
| API | FastAPI (leichtgewichtiger REST-Wrapper) |
| Sprache | Python 3.12+ |

### API

Ein einziger Endpunkt:

```
POST /transcribe
Content-Type: multipart/form-data

Parameter:
  - file: Audio-Datei (WebM, WAV, MP3, etc.)
  - language: "fr" (Default)

Response:
{
  "text": "Bonjour, comment allez-vous ?",
  "segments": [
    {
      "start": 0.0,
      "end": 1.5,
      "text": "Bonjour,",
      "confidence": 0.95
    },
    {
      "start": 1.5,
      "end": 3.2,
      "text": "comment allez-vous ?",
      "confidence": 0.91
    }
  ],
  "language": "fr",
  "confidence": 0.93
}
```

Die Segmente mit Zeitstempeln und Confidence-Werten ermöglichen dem Backend eine granulare Auswertung der Aussprache (z.B. welche Wörter unsicher erkannt wurden).

### Docker-Konfiguration

```dockerfile
# whisper/Dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Modell beim Build herunterladen (Cache im Image)
RUN python -c "from faster_whisper import WhisperModel; WhisperModel('base', compute_type='int8')"

EXPOSE 9000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
```

### Konfiguration per Umgebungsvariablen

```env
WHISPER_MODEL=base          # base, small, medium, large-v3
WHISPER_COMPUTE_TYPE=int8   # int8 (CPU), float16 (GPU)
WHISPER_LANGUAGE=fr         # Default-Sprache
```

---

## Docker Compose

```yaml
# docker-compose.yml
services:
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
    environment:
      - API_URL=http://backend:8000

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - whisper
    volumes:
      - db-data:/app/data
    env_file:
      - .env
    environment:
      - DATABASE_URL=sqlite:///data/coach.db
      - WHISPER_URL=http://whisper:9000

  whisper:
    build: ./whisper
    ports:
      - "9000:9000"
    environment:
      - WHISPER_MODEL=base
      - WHISPER_COMPUTE_TYPE=int8
      - WHISPER_LANGUAGE=fr

volumes:
  db-data:
```

### Starten

```bash
# .env-Datei anlegen mit LLM-Konfiguration
cp .env.example .env
# API-Key und Modell eintragen

# System starten
docker compose up --build

# Zugriff über Browser
open http://localhost:5173
```

---

## Verzeichnisstruktur

```
coach-francais/
├── docker-compose.yml
├── .env.example
├── .env                          # Nicht im Git (enthält API-Key)
├── .gitignore
├── Requirements.md
├── Architecture.md
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/
│       │   └── index.js
│       ├── stores/              # Pinia Stores
│       │   ├── user.js
│       │   ├── plan.js
│       │   └── lesson.js
│       ├── composables/         # Vue Composables
│       │   ├── useTTS.js        # Text-to-Speech (Web Speech API)
│       │   ├── useRecorder.js   # Mikrofon-Aufnahme
│       │   └── useApi.js        # Backend-Kommunikation
│       ├── components/
│       │   ├── MainMenu.vue
│       │   ├── PlanCreator.vue
│       │   ├── LessonView.vue
│       │   ├── DialogPlayer.vue
│       │   ├── ExerciseFillBlank.vue
│       │   ├── ExerciseMultipleChoice.vue
│       │   ├── ExerciseReorder.vue
│       │   ├── ExerciseMatch.vue
│       │   ├── ExerciseFreeAnswer.vue
│       │   ├── ExerciseTransform.vue
│       │   ├── GrammarBox.vue
│       │   ├── ProgressView.vue
│       │   └── AudioRecorder.vue
│       └── views/
│           ├── HomeView.vue
│           ├── PlanView.vue
│           ├── PracticeView.vue
│           └── ProgressView.vue
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   └── app/
│       ├── main.py              # FastAPI-App
│       ├── config.py            # Settings (env vars)
│       ├── database.py          # SQLite-Verbindung
│       ├── models/              # SQLAlchemy/SQLModel
│       │   ├── user.py
│       │   ├── lesson.py
│       │   ├── plan.py
│       │   ├── exercise.py
│       │   └── progress.py
│       ├── routers/             # API-Endpunkte
│       │   ├── plan.py
│       │   ├── lessons.py
│       │   ├── exercises.py
│       │   ├── speech.py
│       │   ├── progress.py
│       │   └── settings.py
│       ├── services/            # Geschäftslogik
│       │   ├── llm.py           # LLM-Client (OpenAI SDK)
│       │   ├── plan_generator.py
│       │   ├── lesson_generator.py
│       │   ├── exercise_evaluator.py
│       │   ├── pronunciation.py # Transkription vs. Zieltext
│       │   └── progress_tracker.py
│       └── prompts/             # LLM System-Prompts
│           ├── plan.py
│           ├── lesson.py
│           ├── exercise.py
│           └── evaluation.py
│
└── whisper/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py              # FastAPI-App mit /transcribe
        └── model.py             # Faster-Whisper Modell-Laden
```

---

## Datenfluss

### Trainingsplan erstellen

```
Nutzer                  Frontend              Backend                LLM
  │                        │                     │                    │
  │  Zielniveau, Themen,   │                     │                    │
  │  Schwerpunkte, Zeit    │                     │                    │
  │───────────────────────▶│                     │                    │
  │                        │  POST /api/plan     │                    │
  │                        │────────────────────▶│                    │
  │                        │                     │  chat.completions  │
  │                        │                     │───────────────────▶│
  │                        │                     │   Strukturierter   │
  │                        │                     │◀──Plan (JSON)──────│
  │                        │                     │                    │
  │                        │                     │  In DB speichern   │
  │                        │                     │                    │
  │                        │◀───Plan-Übersicht───│                    │
  │◀───────────────────────│                     │                    │
```

### Interaktiv üben (Dialog nachsprechen)

```
Nutzer                  Frontend              Backend              Whisper
  │                        │                     │                    │
  │  Lektion starten       │                     │                    │
  │───────────────────────▶│                     │                    │
  │                        │  GET /api/lessons/2 │                    │
  │                        │────────────────────▶│                    │
  │                        │◀──Dialog-Daten──────│                    │
  │                        │                     │                    │
  │  ◀── TTS im Browser ──│                     │                    │
  │     "Bonjour Paul !"   │                     │                    │
  │                        │                     │                    │
  │  🎤 Nutzer spricht     │                     │                    │
  │───Audio-Blob──────────▶│                     │                    │
  │                        │  POST /api/speech/  │                    │
  │                        │  transcribe         │                    │
  │                        │────────────────────▶│                    │
  │                        │                     │  POST /transcribe  │
  │                        │                     │───────────────────▶│
  │                        │                     │◀──Transkription────│
  │                        │                     │                    │
  │                        │                     │  Vergleich mit     │
  │                        │                     │  Zieltext +        │
  │                        │                     │  Feedback (LLM)    │
  │                        │                     │                    │
  │                        │◀──Korrektur─────────│                    │
  │◀───────────────────────│                     │                    │
  │  "Très bien!" oder     │                     │                    │
  │  "Attention: ..."      │                     │                    │
```

---

## LLM-Konfiguration im Detail

Das externe LLM ist die zentrale Intelligenz des Coaches – es generiert Trainingspläne, erstellt Lektionsinhalte, formuliert Übungen und gibt Feedback. Die Konfiguration erfolgt auf **drei Ebenen**, die aufeinander aufbauen:

### Ebene 1: Ersteinrichtung per `.env`-Datei

Beim ersten Start legt der Nutzer die Datei `.env` im Projektverzeichnis an (Vorlage: `.env.example`). Hier werden **Endpunkt, API-Key und Default-Modell** festgelegt:

```env
# ── LLM-Konfiguration ──────────────────────────────

# 1. API-Endpunkt (Base-URL)
#    Muss auf eine OpenAI-kompatible Chat-Completions-API zeigen.
#    Der Pfad /chat/completions wird vom SDK automatisch angehängt.
LLM_API_BASE_URL=https://opencode.ai/inference/openai/v1

# 2. API-Key
#    Authentifizierung gegenüber dem Provider.
LLM_API_KEY=sk-your-key-here

# 3. Modellname
#    Exakt so, wie der Provider das Modell benennt.
#    OpenCode Console ohne Prefix, z.B. "claude-sonnet-5-5".
LLM_MODEL=claude-sonnet-5-5

# 4. Generierungsparameter (Optional, Defaults siehe unten)
LLM_TEMPERATURE=0.7       # 0.0 = deterministisch, 1.0 = kreativ
LLM_MAX_TOKENS=4096        # Max. Antwortlänge in Tokens
```

Diese Werte werden beim Start des Backend-Containers gelesen und als Default verwendet.

### Ebene 2: Modellwechsel über die Weboberfläche (Laufzeit)

In der Weboberfläche gibt es unter **Einstellungen** eine LLM-Konfigurationsseite. Dort kann der Nutzer **ohne Container-Neustart**:

- Das **Modell wechseln** (Eingabefeld für den Modellnamen)
- Die **Generierungsparameter anpassen** (Temperature, Max Tokens)
- Die **Verbindung testen** (Test-Aufruf an die API)

```
┌─────────────────────────────────────────────────┐
│  Einstellungen > LLM-Konfiguration              │
│                                                  │
│  API-Endpunkt:  https://opencode.ai/inference/openai/v1 │
│                 (nur per .env änderbar)          │
│                                                  │
│  API-Key:       sk-••••••••••••••••              │
│                 (nur per .env änderbar)          │
│                                                  │
│  Modell:        [claude-sonnet-5-5            ]  │
│                                                  │
│  Temperature:   [0.7____]                        │
│  Max Tokens:    [4096___]                        │
│                                                  │
│  [🔄 Verbindung testen]   Status: ✅ Verbunden   │
│  [💾 Speichern]                                  │
└─────────────────────────────────────────────────┘
```

**Sicherheitshinweis:** API-Endpunkt und API-Key sind **nur per `.env`-Datei** änderbar (nicht über die UI), um zu verhindern, dass Credentials versehentlich an einen falschen Endpunkt gesendet werden.

### Ebene 3: Backend-Settings-Objekt

Im Backend werden alle LLM-Einstellungen in einem zentralen **Pydantic-Settings-Objekt** zusammengeführt. Die Werte kommen initial aus der `.env`-Datei und können zur Laufzeit per API-Endpunkt überschrieben werden:

```python
# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM
    llm_api_base_url: str = "https://opencode.ai/inference/openai/v1"
    llm_api_key: str = ""
    llm_model: str = "claude-sonnet-5-5"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    # Whisper
    whisper_url: str = "http://whisper:9000"

    # DB
    database_url: str = "sqlite:///data/coach.db"

    # Allgemein
    tts_speed: float = 0.85
    log_level: str = "info"

    class Config:
        env_file = ".env"
```

Die Laufzeit-Änderungen (Modell, Temperature, Max Tokens) werden in der SQLite-Datenbank persistiert und beim nächsten Start wieder geladen. Die `.env`-Werte dienen nur als initiale Defaults.

### API-Endpunkte für LLM-Konfiguration

| Endpunkt | Methode | Beschreibung |
|---|---|---|
| `GET /api/settings/llm` | GET | Aktuelle LLM-Konfiguration abrufen (API-Key wird maskiert) |
| `PUT /api/settings/llm` | PUT | Modell, Temperature, Max Tokens ändern |
| `POST /api/settings/llm/test` | POST | Testanfrage an die API senden und Ergebnis zurückmelden |

**Beispiel – Modell wechseln:**
```json
PUT /api/settings/llm
{
    "llm_model": "gpt-6.2-sol",
    "llm_temperature": 0.5,
    "llm_max_tokens": 8192
}
```

**Beispiel – Verbindung testen:**
```json
POST /api/settings/llm/test

Response (Erfolg):
{
    "status": "ok",
    "model": "gpt-6.2-sol",
    "response_time_ms": 842,
    "message": "Connexion réussie."
}

Response (Fehler):
{
    "status": "error",
    "error": "401 Unauthorized – API-Key ungültig."
}
```

### Kompatible Provider und Modelle

Da das System das **OpenAI SDK** mit konfigurierbarer `base_url` nutzt, funktioniert jeder Provider, der das OpenAI-Chat-Completions-Format unterstützt:

| Provider | `LLM_API_BASE_URL` | Beispiel-Modelle |
|---|---|---|
| **OpenCode Console** | `https://opencode.ai/inference/openai/v1` | `claude-sonnet-5-5`, `claude-opus-5-5`, `gemini-4-argon`, `gpt-6.2-sol` |
| **OpenRouter** | `https://openrouter.ai/api/v1` | Provider-Prefix, z.B. `anthropic/claude-sonnet-5.5` |
| **OpenAI direkt** | `https://api.openai.com/v1` | aktuelle OpenAI-ID, z.B. `gpt-6.2-sol` |
| **Lokales Modell (Ollama)** | `http://host.docker.internal:11434/v1` | `gemma4` |
| **Lokales Modell (LM Studio)** | `http://host.docker.internal:1234/v1` | Beliebiges geladenes Modell |

### Empfohlene Modelle nach Einsatzzweck

Nicht jede Aufgabe erfordert das gleiche Modell. Für die Zukunft ist eine **pro-Funktion-Konfiguration** denkbar, initial wird aber ein einzelnes Modell für alles verwendet:

| Aufgabe | Anforderung | Empfehlung |
|---|---|---|
| Trainingsplan generieren | Strukturiertes Reasoning, JSON-Output | `claude-sonnet-5-5` oder `claude-opus-5-5` |
| Dialoge erstellen | Natürliches Französisch, kulturelle Nuancen | `claude-sonnet-5-5` oder `gemini-4-argon` |
| Übungen generieren | Korrektes Französisch, Grammatik-Wissen | `claude-sonnet-5-5` |
| Aussprache-Feedback | Textvergleich, kurze Antworten | `claude-haiku-5-5` oder `gpt-6-luna` |
| Fehleranalyse | Mustererkennung über Fehlerliste | Mittleres Modell |

### Validierung beim Start

Beim Start des Backend-Containers prüft das System:

1. **`LLM_API_BASE_URL` gesetzt?** – Falls leer, startet der Container mit Warnung. Die App ist nutzbar, aber Trainingsplan-Erstellung und Übungsgenerierung sind deaktiviert.
2. **`LLM_API_KEY` gesetzt?** – Falls leer, ebenfalls Warnung.
3. **Verbindungstest:** Ein optionaler Health-Check (`GET /models` am API-Endpunkt) prüft, ob der Provider erreichbar ist. Bei Fehler wird geloggt, der Container startet aber trotzdem.

```
[INFO]  LLM-Provider: https://opencode.ai/inference/openai/v1
[INFO]  LLM-Modell:   claude-sonnet-5-5
[INFO]  LLM-Status:   ✅ Verbunden (Response: 203ms)
```

oder:

```
[WARN]  LLM-Status: ❌ Nicht erreichbar (Timeout nach 5s)
[WARN]  Trainingsplan-Erstellung und Übungsgenerierung sind nicht verfügbar.
```

---

## Konfiguration (.env.example)

```env
# ── LLM-Konfiguration ──────────────────────────────
# Endpunkt der OpenAI-kompatiblen API
# Siehe Abschnitt "Kompatible Provider" für Beispiele.
LLM_API_BASE_URL=https://opencode.ai/inference/openai/v1

# API-Key (vom Provider bereitgestellt)
LLM_API_KEY=sk-your-key-here

# Modellname (exakt wie vom Provider benannt, ohne Prefix)
# Beispiele: claude-sonnet-5-5, claude-opus-5-5, gemini-4-argon, gpt-6.2-sol
LLM_MODEL=claude-sonnet-5-5

# Generierungsparameter
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096

# ── Whisper-Konfiguration ──────────────────────────
WHISPER_MODEL=base
WHISPER_COMPUTE_TYPE=int8
WHISPER_LANGUAGE=fr

# ── Datenbank ──────────────────────────────────────
DATABASE_URL=sqlite:///data/coach.db

# ── Allgemein ──────────────────────────────────────
TTS_SPEED=0.85
LOG_LEVEL=info
```
