# PRD - ClipEngine (Video Repurposing Tool)

## 1. Problem Statement

Content creators need to repurpose long-form horizontal (16:9) videos into short-form vertical (9:16) clips for TikTok, Reels, and Shorts.
Manual editing, face-tracking, and captioning are time-consuming and require technical skill most solo creators do not have.

## 2. Target Audience

- Solo content creators, podcasters, and educators with long-form video content.
- Technical level is low - users expect an "upload and download" experience with zero configuration.

## 3. Core User Flow

1. User uploads an MP4 file through a simple web interface.
2. System checks for duplicate uploads using file hash - if already processed, return cached results instantly.
3. System extracts audio, transcribes it, and identifies 3-5 high-engagement moments using an LLM.
4. System trims, crops to 9:16 with face-tracking, burns in captions and titles, and optimizes for streaming.
5. User downloads the finished vertical clips.

## 4. Functional Requirements

### 4.1 Ingestion

- User uploads video via a Bootstrap frontend.
- Maximum file size: 100 MB.
- Display estimated processing time based on file size.

### 4.2 Deduplication

- Calculate file hash on upload.
- Query Supabase for existing hash - if found, return cached results immediately without reprocessing.
- This must happen before any API calls to save cost.

### 4.3 Transcription

- Convert uploaded video to audio using ImageKit.
- Send audio to Groq Whisper API (whisper-large-v3-turbo) for timestamped transcription.

### 4.4 Moment Selection

- Send transcript to Groq LLM (llama-3.3-70b-versatile or equivalent Groq-supported model).
- Prompt the LLM to identify 3-5 high-engagement segments - hooks, punchlines, key insights.
- LLM returns: start time, end time, suggested title, suggested caption for each segment.

### 4.5 Video Processing (ImageKit)

- Trim video to selected timestamps.
- Smart crop to 9:16 using face detection to keep the speaker centered.
- Burn in generated captions and titles as overlay.
- Convert to streamable MP4 (H.264/AAC).

### 4.6 Delivery

- Display all generated clips with preview thumbnails.
- Provide individual download links for each clip.

## 5. Data Model (Supabase)

### Table: videos

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| file_hash | Text, Unique | For deduplication |
| original_imagekit_id | Text | Reference to uploaded file |
| status | Text | 'processing', 'completed', 'failed' |
| transcript_data | JSONB | Stores Whisper output |
| clips_data | JSONB | LLM-selected moments and resulting ImageKit URLs |
| created_at | Timestamp | Auto-generated |

## 6. Non-Functional Requirements

### Performance

- Transcription + LLM analysis must complete within 30 seconds for a 10-minute video.
- Total end-to-end processing (upload to download-ready) under 5 minutes for a 10-minute video.
- File size limit: 100 MB.

### Cost

- Pipeline must cost less than $0.05 per minute of video processed.
- Total API cost per video must stay under $0.10.
- Deduplication must prevent redundant API calls.

### Scalability

- Flask backend must handle processing asynchronously - do not block the UI while video processes.
- Use polling or a similar mechanism to update the user on processing status.

### Frontend

- Fully responsive using Bootstrap 5 via CDN.
- No complex JS frameworks - vanilla JavaScript only for API calls and UI interactions.

## 7. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, Bootstrap 5 (CDN), Vanilla JavaScript |
| Backend | Python Flask |
| AI - Transcription | Groq Whisper API (whisper-large-v3-turbo) |
| AI - Moment Selection | Groq LLM (Llama 3.3 70B Versatile) |
| Media Processing | ImageKit.io (storage, smart crop, captioning, CDN) |
| Database | Supabase (PostgreSQL) |
| Auth | None for MVP |

## 8. Edge Cases

- **No face detected:** Default to center-crop instead of face-tracking.
- **Audio-only or static video:** Skip face crop, process audio and captions only.
- **Short videos (under 30 seconds):** Return the entire video as a single clip rather than splitting.
- **API rate limits:** Implement retry logic with exponential backoff for Groq and ImageKit.
- **Duplicate uploads:** Catch via hash check before any API call is made.
- **Processing failure:** Set status to 'failed', display a clear error to the user, allow re-upload.

## 9. Out of Scope (MVP)

- User authentication and accounts.
- Batch upload of multiple videos.
- Manual editing or trimming by the user.
- Custom caption styling or font selection.
- Platform-specific export presets (TikTok vs Reels vs Shorts).
- Analytics or usage dashboards.

## 10. Success Criteria

- User can upload a 10-minute video and receive 3 vertical clips with captions in under 5 minutes.
- 80% of auto-selected clips are deemed usable by the user.
- Total API cost per video stays under $0.10.

## Appendix: File Size vs Duration Reference

Use this in frontend UI copy to set user expectations on the 100 MB limit.

| Quality | Resolution | Approximate Duration at 100 MB |
|---|---|---|
| Low | 144p-240p | 20-30 minutes |
| Standard | 720p | ~2.5 minutes |
| High | 1080p | 1-1.5 minutes |
| Very High | 4K | 20-40 seconds |