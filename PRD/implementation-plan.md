# ClipEngine implementation plan

## Summary

Build a Flask web app that lets a low-technical-skill creator upload one MP4, checks the file hash before any paid API calls, processes new videos asynchronously, and returns 3-5 vertical captioned clips for download.

The repo currently has no app scaffold and is not a Git repository, so implementation starts with repo hygiene and small commits.

Use RQ + Redis for background jobs because the PRD requires non-blocking processing, status polling, retries, and failure tracking.

Current docs confirm the planned provider capabilities.

ImageKit supports URL-based video trim, crop, thumbnails, overlays, and audio extraction.

Groq supports timestamped Whisper output with `verbose_json`.

`llama-3.3-70b-versatile` is currently listed as a production model.

Provider references:

- ImageKit video transformations: https://imagekit.io/docs/video-transformation
- ImageKit overlays: https://imagekit.io/docs/add-overlays-on-videos
- ImageKit resize and crop: https://imagekit.io/docs/video-resize-and-crop
- ImageKit audio transformations: https://imagekit.io/docs/audio-transformations
- Groq speech-to-text: https://console.groq.com/docs/speech-to-text
- Groq models: https://console.groq.com/docs/models

## Phased work with checkpoints

### Phase 0: Repository and project foundation ✅

- Initialize Git before any app work because the workspace is currently not a repository.
- Add a first commit containing only the existing documentation state.
- Create the Flask project scaffold with `src/`, `tests/`, and minimal app files.
- Add `.gitignore`, `.env.example`, dependency manifest, and local run instructions.
- Use small commits and stop for a commit checkpoint after this phase.

Checkpoint:

- Flask app starts locally.
- `/health` returns OK.
- No external APIs are called.
- User can inspect the initial scaffold before feature work continues.

### Phase 1: Core app shell and upload UI

- Build a single Bootstrap 5 page with vanilla JavaScript.
- Include MP4 file selection, 100 MB validation, estimated processing time, upload progress, status area, and results area.
- Use a simple file-size estimate such as `max(30 seconds, sizeMB * 2.5 seconds)` for MVP copy, clearly marked as an estimate.
- Add backend request size limits and MP4 validation.
- Do not add auth, accounts, dashboards, batch upload, or custom caption controls.

Checkpoint:

- User can choose an MP4 and see validation before upload.
- Files over 100 MB are rejected client-side and server-side.
- UI is responsive on mobile and desktop.
- Commit with message like `Add upload page`.

### Phase 2: Supabase schema, API contract, and deduplication

Public API shape:

- `POST /api/videos` accepts `multipart/form-data` with `video`.
- `POST /api/videos` streams the upload to temp storage while calculating SHA-256.
- `POST /api/videos` checks Supabase by `file_hash` before ImageKit or Groq calls.
- `POST /api/videos` returns cached completed clips immediately when the hash already exists.
- `POST /api/videos` returns existing processing status when the same hash is already in progress.
- `POST /api/videos` creates a new `processing` row and enqueues a job only for new files.
- `GET /api/videos/<video_id>` returns `id`, `status`, `current_step`, `progress_percent`, `error_message`, `clips`, and timestamps.

Supabase table additions beyond the PRD:

- Keep required PRD fields: `id`, `file_hash`, `original_imagekit_id`, `status`, `transcript_data`, `clips_data`, and `created_at`.
- Add `source_filename`, `file_size_bytes`, `duration_seconds`, `current_step`, `progress_percent`, `error_message`, `job_id`, and `updated_at`.
- Use a unique index on `file_hash`.

Checkpoint:

- Duplicate upload returns cached or in-progress data without hitting mocked ImageKit or Groq clients.
- New upload creates one Supabase row and one RQ job.
- Commit with message like `Add upload deduplication`.

### Phase 3: Async worker pipeline

- Add Redis and RQ worker setup.
- Upload the original MP4 to ImageKit.
- Extract audio using ImageKit audio extraction with video codec set to none.
- Send audio URL or file to Groq Whisper with `whisper-large-v3-turbo`, `verbose_json`, and segment timestamps.
- Store transcript JSON in Supabase.
- Update status and progress after every worker step.
- Add exponential backoff retries for Groq and ImageKit calls.
- On failure, set status to `failed`, store a clear error message, and allow re-upload.

Checkpoint:

- A mocked worker processes a fake job through all transcript states.
- Failed provider calls move the row to `failed`.
- UI polling shows progress and failure states.
- Commit with message like `Add async transcription pipeline`.

### Phase 4: Moment selection

- Send transcript segments to Groq LLM using `llama-3.3-70b-versatile`.
- Require structured JSON output with an array of 3-5 clips.
- Each clip must include `start_time`, `end_time`, `title`, `caption`, and `reason`.
- Validate LLM output before video processing.
- Times must be inside video duration.
- End time must be after start time.
- Clips should not overlap heavily.
- Short videos under 30 seconds return one full-length clip.
- Store selected moments in `clips_data` before rendering begins.

Checkpoint:

- Transcript fixture produces validated clip selections.
- Invalid LLM JSON or bad timestamps trigger a retry, then a clean failure if still invalid.
- Short video fixture returns one clip.
- Commit with message like `Add moment selection`.

### Phase 5: ImageKit clip rendering

- For each selected segment, build ImageKit transformation URLs that trim to selected start and end.
- Crop output to 9:16 at 1080x1920.
- Apply smart person crop first.
- Fall back to center crop if smart crop probing fails.
- Add title as a text overlay.
- Add captions through generated subtitle overlay files.
- Output streamable MP4 using H.264 video and AAC audio.
- Generate WebVTT or SRT caption files from Whisper timestamps and upload them to ImageKit for subtitle overlays.
- Generate thumbnail URLs from each clip start time.
- Warm each transformed clip URL from the worker so processing finishes before status becomes `completed`.
- Store final clip URLs, thumbnail URLs, titles, captions, and timing metadata in `clips_data`.

Checkpoint:

- Worker produces previewable clip URLs with thumbnails.
- Static or audio-only video still produces captions and a center-cropped or non-face-tracked result.
- No-face behavior falls back without failing the job.
- Commit with message like `Add ImageKit clip rendering`.

### Phase 6: Results UI, polling, and downloads

- Frontend polls `GET /api/videos/<id>` until status is `completed` or `failed`.
- Display clip cards with thumbnail, title, preview video, duration, and download button.
- Show clear failed-state messaging and allow re-upload.
- For duplicates, skip progress UI and render cached results immediately.
- Keep the UI simple and Bootstrap-native with no frontend framework.

Checkpoint:

- End user flow works from upload to downloadable clips with mocked services.
- Duplicate upload instantly shows existing clips.
- Mobile and desktop layouts are visually checked.
- Commit with message like `Add clip results UI`.

### Phase 7: End-to-end validation and hardening

- Add unit tests for hashing, validation, Supabase repository logic, LLM output validation, and ImageKit URL generation.
- Add integration tests with mocked Groq, ImageKit, Supabase, Redis, and RQ.
- Add one E2E test for the full browser flow using a small sample MP4 and mocked provider responses.
- Add manual test cases in `test-cases.md`.
- Cover successful upload, duplicate upload, file too large, short video, no face detected, static or audio-only video, Groq rate limit, ImageKit failure, and worker crash or retry.
- Confirm cost guardrails by logging estimated video duration, provider calls made, retries, and whether deduplication skipped paid calls.

Checkpoint:

- Tests pass locally.
- E2E flow is verified.
- Processing failure paths are visible and understandable.
- Commit with message like `Add MVP test coverage`.

## Assumptions and defaults

- RQ + Redis is the async implementation.
- Git will be initialized before implementation starts.
- The MVP has no auth and no batch uploads.
- Supabase stores metadata only.
- Videos and subtitle assets live in ImageKit.
- Temp uploaded files are deleted after the worker no longer needs them.
- Final clips are represented by warmed ImageKit transformation URLs, not separate manually rendered local files.
- Default output target is 1080x1920 MP4 with H.264 video and AAC audio.
- External API keys come from environment variables only.
