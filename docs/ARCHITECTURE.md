# AI Shorts Tool Architecture

## 1. What We Are Building

This project is a web application that turns one long 16:9 video into multiple short 9:16 clips for platforms like TikTok, Instagram Reels, and YouTube Shorts.

The user flow is:

1. A creator uploads a long video.
2. The app stores the video in ImageKit.
3. The backend transcribes the video audio with Groq Whisper.
4. The backend asks a Groq LLM to find the best short-form moments.
5. The app creates vertical clip preview URLs using ImageKit transformations.
6. The creator reviews, edits, previews, and downloads the clips.

The goal is not only to build the app. The goal is to understand each piece well enough to explain it clearly.

## 2. Technology Choices

### Frontend: Plain JavaScript and Bootstrap

Plain JavaScript means we will write browser code without React, Vue, or another frontend framework.

Bootstrap gives us ready-made UI patterns like buttons, forms, layout grids, cards, modals, and progress bars.

Why we use this:

- It keeps the frontend easier to learn.
- It avoids a build system at the beginning.
- It is enough for upload forms, progress screens, and clip review pages.

Simpler alternative:

- Use plain HTML with almost no styling.
- We are not choosing that because the app should feel clean and usable for non-technical content creators.

More advanced alternative:

- Use React or Vue.
- We are not choosing that for v1 because the learning goal is to understand the full request flow first.

### Backend: Python Flask

Flask is a lightweight Python web framework. It receives browser requests, returns pages, exposes API routes, talks to the database, and starts background jobs.

Why we use this:

- It is beginner-friendly.
- It makes request/response flow easy to see.
- It works well for small and medium web apps.

Simpler alternative:

- Use only static HTML and JavaScript.
- We cannot do that because API keys, database writes, background jobs, and AI calls need a backend.

### Database: Supabase Postgres with SQLAlchemy

Supabase gives us a managed PostgreSQL database in the cloud. PostgreSQL stores permanent app data, and SQLAlchemy lets Python code work with database tables through Python classes.

We will store:

- uploaded video metadata,
- a `file_hash` fingerprint for duplicate detection,
- ImageKit file IDs and URLs,
- processing job status,
- transcript segments,
- generated clips,
- titles and captions,
- prompt runs,
- user ownership later.

Why we use this:

- App state must survive server restarts and deployments.
- Supabase avoids local database server setup while still teaching real Postgres.
- SQLAlchemy keeps the Flask code close to normal backend patterns.
- `file_hash` lets the app detect the same video later and reuse saved transcript/clips instead of paying to process it again.
- ImageKit stores the actual video file; Supabase stores the memory of what happened to that file.

Simpler alternative:

- Use SQLite locally.
- SQLite is useful as a fallback, but it is not the main target because this app is meant to deploy and support many users.

Rejected alternative:

- Use Firebase Firestore as the main database.
- We are not choosing that because Firestore is a document database and would move us away from the Flask + SQLAlchemy + Postgres learning path.

### Background Jobs: Redis and RQ

Some work takes too long for a normal web request. Transcribing a video, asking an LLM to analyze it, and preparing clip URLs may take many seconds or minutes.

Redis is an in-memory data store. RQ is a Python job queue that uses Redis.

Why we use this:

- Flask can quickly say, "Your job has started."
- The worker can process the video in the background.
- The frontend can poll job status while the user waits.

Simpler alternative:

- Do all work inside one Flask request.
- We are not choosing that because long requests are unreliable and can time out.

More advanced alternative:

- Use Celery.
- We are not choosing that for v1 because RQ is easier to learn and enough for this project.

### Media Layer: ImageKit

ImageKit stores uploaded videos and creates transformed video URLs.

We will use it for:

- direct browser video upload,
- video storage,
- vertical 9:16 face crop,
- trimming clips,
- subtitle overlays,
- streamable preview URLs,
- downloadable video URLs.

Why we use this:

- Flask should not store large video files.
- Video processing is expensive and specialized.
- ImageKit URL transformations let us create clip variants without manually rendering every file ourselves.

Important detail:

- ImageKit transformations are usually URL-based. That means the app stores transformation URLs, not necessarily a new physical video file for every clip.

### AI Layer: Groq Whisper and Groq LLM

Groq Whisper transcribes video audio into text with timestamps.

The Groq LLM reads transcript segments and chooses good short-form clips.

Why we use this:

- Transcript timestamps tell us where interesting moments happen.
- The LLM can reason about hooks, useful moments, emotional highlights, and clean clip boundaries.
- Titles, captions, and hashtags can be generated from the same transcript context.

Default models:

- Transcription: `whisper-large-v3-turbo`
- Clip selection and metadata: `llama-3.3-70b-versatile`

## 3. High-Level Request Flow

### Upload Flow

1. The browser asks Flask for an ImageKit upload signature.
2. Flask creates a short-lived signed upload response.
3. The browser uploads the video directly to ImageKit.
4. ImageKit returns file metadata.
5. The browser sends that metadata to Flask.
6. Flask stores a `Video` record in Supabase Postgres.
7. The `Video` record includes a `file_hash` so duplicate uploads can reuse saved results.

Why this matters:

- The large video does not pass through Flask.
- Uploads are faster and cheaper.
- The backend only stores metadata and references.

### Generate Shorts Flow

1. The user clicks "Generate Shorts."
2. The browser sends a request to Flask.
3. Flask checks Supabase for an existing completed video with the same `file_hash`.
4. If completed results already exist, Flask returns the saved clips without reprocessing.
5. If no completed results exist, Flask creates a `ProcessingJob` database record.
6. Flask puts a job into RQ.
7. The RQ worker starts processing.
8. The frontend polls Flask for job progress.
9. When processing finishes, Flask returns generated clips.

Why this matters:

- The web app stays responsive.
- The user can refresh the page and still see job state.
- Failures can be stored and shown clearly.

### Worker Processing Flow

1. Load the `Video` record.
2. Get the ImageKit video URL.
3. Send the audio/video URL to Groq Whisper.
4. Normalize and save transcript segments.
5. Send transcript segments to Groq LLM.
6. Validate the returned clip JSON.
7. Generate subtitle files from transcript timestamps.
8. Upload subtitle files to ImageKit.
9. Build ImageKit transformation URLs for each clip.
10. Save `Clip` records.
11. Mark the job as complete.

## 4. Core Data Models

### User

Represents the person using the app.

V1 can start with one admin user, but the schema should be ready for invite-only users later.

Fields:

- `id`
- `email`
- `created_at`

### Video

Represents one uploaded long video.

Fields:

- `id`
- `user_id`
- `file_hash`
- `imagekit_file_id`
- `original_url`
- `filename`
- `duration_seconds`
- `status`
- `created_at`

### ProcessingJob

Represents background work for one video.

Fields:

- `id`
- `video_id`
- `status`
- `progress_step`
- `error_message`
- `created_at`
- `updated_at`

Statuses:

- `queued`
- `running`
- `failed`
- `done`

### TranscriptSegment

Represents a timestamped piece of transcript.

Fields:

- `id`
- `video_id`
- `start_seconds`
- `end_seconds`
- `text`
- `raw_metadata`

### Clip

Represents one generated short.

Fields:

- `id`
- `video_id`
- `start_seconds`
- `end_seconds`
- `score`
- `reason`
- `title`
- `caption`
- `hashtags`
- `subtitle_file_id`
- `preview_url`
- `selected`

### PromptRun

Represents one AI prompt execution.

Fields:

- `id`
- `video_id`
- `prompt_name`
- `prompt_version`
- `model`
- `input_summary`
- `output_json`
- `created_at`

Why this table matters:

- It helps debug AI behavior.
- It helps future engineers understand what prompt produced which result.
- It supports recruiter-facing traceability.

## 5. API Routes

### Page Routes

- `GET /`
  - Shows the upload page.
- `GET /videos/<video_id>`
  - Shows video processing or result state.

### JSON API Routes

- `POST /api/imagekit/auth`
  - Returns upload authentication for ImageKit.
- `POST /api/videos`
  - Saves uploaded video metadata after ImageKit upload.
- `GET /api/videos`
  - Lists uploaded videos.
- `GET /api/videos/<video_id>`
  - Returns one video and its clips.
- `POST /api/videos/<video_id>/generate`
  - Starts the background generation job.
- `GET /api/jobs/<job_id>`
  - Returns job status and progress.
- `PATCH /api/clips/<clip_id>`
  - Updates editable clip fields.
- `POST /api/clips/<clip_id>/regenerate-metadata`
  - Regenerates title, caption, and hashtags only.

## 6. Step-by-Step Implementation Phases

### Phase 0 ✅: Project Rules and Architecture

Build:

- `RULES.md`
- `docs/ARCHITECTURE.md`
- `prompts/project-prompts.md`

Test:

- Open the files and confirm they explain the project clearly.

### Phase 1 ✅: Minimal Flask App

Build:

- Flask app factory.
- One home page.
- One health check route.
- Basic Bootstrap layout.

Test:

- Run Flask locally.
- Open the home page.
- Confirm health check returns success.

### Phase 2 ✅: Configuration and Environment Variables

Build:

- config loading for Flask.
- `DATABASE_URL` is prepared for Supabase Postgres in Phase 3.
- Groq, ImageKit, and Redis settings are optional future values until their phases begin.

Test:

- Start the app with local environment variables.
- Confirm missing required config gives a clear error.

### Phase 3 ✅: Supabase Postgres Setup

Build:

- Create or connect a Supabase project.
- Put the Supabase Postgres connection string in `DATABASE_URL`.
- Add SQLAlchemy setup.
- Add the first `Video` model with `file_hash` from the start.
- Add migrations so schema changes are tracked.

Test:

- Connect Flask to Supabase Postgres.
- Create the database tables through migrations.
- Insert and read a sample video metadata record with a `file_hash`.

### Phase 4: ImageKit Upload Authentication

Build:

- Backend route that signs ImageKit upload requests.
- Frontend upload form.

Test:

- Request upload auth from the browser.
- Confirm the response contains the values ImageKit needs.

### Phase 5: Direct Video Upload

Build:

- Browser upload to ImageKit.
- Compute or receive a `file_hash` for the selected video.
- Save returned ImageKit metadata and `file_hash` through Flask.
- Check Supabase for duplicate completed videos before starting expensive processing.

Test:

- Upload a small video.
- Confirm ImageKit receives it.
- Confirm Supabase stores the metadata and `file_hash`.
- Confirm a repeated hash can be detected.

### Phase 6: Redis and RQ Job Queue

Build:

- Redis connection.
- RQ worker setup.
- Generate button that creates a background job.
- Job status polling endpoint.

Test:

- Enqueue a fake job.
- Watch the status move from queued to running to done.

### Phase 7: Groq Whisper Transcription

Build:

- Groq transcription service.
- Transcript normalization.
- `TranscriptSegment` saving.

Test:

- Transcribe one short test video.
- Confirm transcript segments have start time, end time, and text.

### Phase 8: Groq LLM Clip Selection

Build:

- Prompt template for selecting clips.
- Strict JSON output validation.
- `Clip` record creation.

Test:

- Send a test transcript.
- Confirm clips are inside the video duration.
- Confirm invalid model output fails clearly.

### Phase 9: Subtitles

Build:

- Convert transcript segments into WebVTT subtitles.
- Upload subtitle file to ImageKit.

Test:

- Generate subtitles for one clip.
- Confirm subtitle timing matches the clip.

### Phase 10: ImageKit Clip URLs

Build:

- Central function that creates ImageKit transformation URLs.
- 9:16 face-aware crop.
- trim start and duration.
- subtitle overlay.

Test:

- Generate one preview URL.
- Open it in the browser.
- Confirm it shows a vertical short with captions.

### Phase 11: Results UI

Build:

- Clip preview cards.
- Editable title.
- Editable caption.
- Editable hashtags.
- Download/open buttons.

Test:

- Generate clips.
- Edit metadata.
- Refresh page and confirm edits remain.

### Phase 12: Deployment Preparation

Build:

- Production config.
- Web service command.
- Worker service command.
- Database migration command.
- Health check endpoint.

Test:

- Deploy web service.
- Deploy worker service.
- Confirm a background job completes in production.

### Phase 13: 50-User Readiness

Build:

- Invite-only login.
- Per-user video ownership.
- Job quotas.
- Max file duration.
- Cost tracking basics.
- Admin job dashboard.

Test:

- Confirm users cannot see each other's videos.
- Confirm quotas prevent accidental cost spikes.
- Confirm failed jobs are visible to the admin.

## 7. Testing Strategy

We will test in layers.

Unit tests:

- transformation URL builder,
- transcript normalization,
- clip validation,
- prompt output parsing.

Integration tests:

- upload metadata save,
- job enqueue,
- transcript save,
- clip creation,
- failed external API handling.

Manual tests:

- upload video,
- generate clips,
- preview vertical clips,
- edit metadata,
- open download URL.

## 8. Current Defaults

- Start without authentication, then add user ownership later.
- Use Supabase Postgres as the main deployed database.
- Store `file_hash` from the first `Video` model version.
- Store actual video files in ImageKit, not in the database.
- Output 9:16 shorts first.
- Use RQ instead of Celery.
- Use Bootstrap and plain JavaScript.
- Use ImageKit as the media system.
- Use Groq for transcription and clip selection.

## 9. Important Risks

### Large Video Files

Risk:

- AI transcription APIs may reject very large files.

Plan:

- Prefer URL-based transcription where possible.
- Add audio extraction and chunking when needed.

### AI Output Quality

Risk:

- The LLM may return invalid JSON or weak clip choices.

Plan:

- Validate every response.
- Store prompt runs.
- Let the user edit and regenerate metadata.

### Cost Control

Risk:

- Video processing and AI calls can become expensive with many users.

Plan:

- Add quotas before inviting 50 users.
- Track job counts and approximate costs.

### User Experience

Risk:

- Creators may not understand technical job states.

Plan:

- Use simple labels like "Uploading," "Finding best moments," and "Preparing previews."
- Keep technical details in expandable debug sections.
