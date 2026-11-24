# Coach Français

Interaktiver Französisch-Coach für eine Person. Der Coach spricht möglichst Französisch, baut aus Zielniveau, Grammatik-Schwerpunkten, Themen und Zeitbudget einen Lektionsplan und übt Alltagssituationen: Dialog hören, nachsprechen, Lücken füllen, frei antworten. Fortschritt und typische Fehler bleiben in einer lokalen SQLite-Datei.

Sprache bleibt lokal. Vorlesen läuft im Browser (Web Speech API), Spracherkennung im Whisper-Container. Nur die Erstellung des Trainingsplans verlässt den Rechner. Lektionen, Übungen, Aussprache-Feedback und Fehleranalyse laufen über Ollama auf dem Host.

## Starten

Voraussetzung: Docker mit Compose, und Ollama auf dem Host (`ollama pull gemma4`).

1. Konfiguration anlegen und den API-Key aus der [OpenCode Console](https://opencode.ai/console) eintragen (Account → Personal API keys). Ein abgelaufener Key muss dort neu erzeugt werden; erneuern durch erneutes Anmelden reicht nicht.

   ```bash
   cp .env.example .env
   ```

2. In `.env` den API-Key setzen. Die Modellnamen stehen nur in `.env.example`: `LLM_MODEL=grok-4.7` für den Plan, `OLLAMA_MODEL=gemma4` für alles andere. Console-IDs ohne Provider-Prefix.

3. Alles bauen und starten:

   Docker Desktop starten, dann

   ```bash
   docker compose up --build
   ```

4. Im Browser öffnen: [http://localhost:5173](http://localhost:5173)

| Dienst | Adresse | Aufgabe |
|---|---|---|
| Frontend | http://localhost:5173 | Vue-Oberfläche, leitet `/api` an das Backend |
| Backend | http://localhost:8000 | FastAPI, Trainingsplan, Übungen, SQLite |
| Whisper | http://localhost:9000 | Faster-Whisper, Französisch, CPU |
| Ollama | http://localhost:11434 | Lokales Modell `gemma4`, nicht im Compose-Stack |

Beim ersten Start lädt der Whisper-Container das Modell `base`. Das dauert. Datenbank und Lernstand liegen im Volume `db-data`.

Anhalten:

```bash
docker compose down
```

Unter **Paramètres** lässt sich nur das Plan-Modell wechseln. Das lokale Modell steht fest in `.env`.

## Modelle

| Aufgabe | Variable | Aktueller Name |
|---|---|---|
| Trainingsplan, extern | `LLM_MODEL` | `grok-4.7` |
| Lektionen, Übungen, Feedback | `OLLAMA_MODEL` | `gemma4` |
| Spracherkennung | `WHISPER_MODEL` | `base` |

`gemma4` ersetzt die alten Ollama-Beispiele `llama3`, `mistral` und `gemma2`. Vor dem ersten Üben einmal `ollama pull gemma4` ausführen. Der Container erreicht Ollama über `host.docker.internal:11434`.

Details zur Aufteilung der Container stehen in [Architecture.md](Architecture.md), der didaktische Ablauf in [Requirements.md](Requirements.md).
