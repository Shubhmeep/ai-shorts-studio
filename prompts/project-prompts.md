# Project Prompts

This file tracks important prompts used to design and build the AI shorts tool. The goal is traceability: future engineers should be able to see what was asked, why it was asked, and what decisions came from it.

## Prompt 0: Initial Product and Architecture Request

Date: 2026-06-27

Purpose:

- Define the product idea.
- Choose the initial architecture.
- Ask for a junior-engineer-friendly explanation.
- Require prompt traceability from the beginning.

Expected output:

- A high-level architecture plan.
- A step-by-step build path.
- A prompts folder with this original prompt recorded.

Decisions requested:

- Use a Python Flask backend.
- Use normal JavaScript and Bootstrap instead of a frontend framework.
- Use Groq Whisper for transcription.
- Use Groq LLM, specifically a 70B model, for clip selection, titles, and captions.
- Use ImageKit for video upload, transformation, captions, streaming, and downloads.
- Build toward deployment and at least 50 users.
- Teach the project so the learner can explain it to recruiters.

Original prompt:

```text
I want to build an AI shorts tool. The basic idea is I want to upload a large file, some standard 16 by 9 video, and then I want to convert that into multiple shorter clips. The idea is that I want to take this long video, I want to generate those shorter clips, and I want to do that by analyzing the audio transcripts. I would like to build this using normal JS, I  was thinking about bootstrap as I do not possess front-end frameworks knowledge and make this a web app, and I want to use the following tools. First, for the transcription of the video, I want to use Whisper from Groq. So, I'll provide a Groq API key. I then want to use groq LLM, specifically the and 70B parameter model, for actually picking out the moments in my video and then generating titles and captions for those particular shorts. Lastly, I want to use ImageKit for handling all of the image and video-related tasks. For example, I want it to reframe the face of the user, I want it to add captions, I want it to give me the streamable video format, and I want it to handle actually uploading my video, allowing me to download it, etc. Can you create a high-level plan and kind of architecture document for this application so we have the context in our project? I plan to deploy this project and learn about development properly, I want to have python flask backend. Ask me any questions that you need before we proceed.  

Few things to note on top:

1. I want you to generate the archtecture in depth if X is being used hy x is being used for a jr engineer who is started dev. 

2. I want a good, clean UI. Easily used by a non tech/content creator. 

3. Make a prompts folder and a md file in it in which you note every prompt being used to make this project. It is easier for traceability and revisiting the project for other engineers. what prompt being used and why? When i said prompts i want i meant: prompt that i am using right now here to do the work like the above decision if we go forward with it. Ok? Add this prompt as well as this is the 0th Prompt.

4. I want to learn and build and deploy this for atleast 50 users. so teach me, help me make the decision i want to show recruiters I know what I built by using AI. 

Is everything clear to you? 
```

## Prompt 1: Tutorial Workflow Rules

Date: 2026-06-27

Purpose:

- Define how the project should be taught and implemented.
- Require small, testable steps.
- Prevent large unexplained code generation.

Expected output:

- A root-level `RULES.md` file.
- A development workflow that prioritizes learning.

Original prompt:

```text
Treat this project as a guided tutorial, not just an implementation task.

As you work:

* Build one small, testable step at a time.
* Before writing code, explain what we are building, why it is needed, and where it fits in the architecture.
* Explain important design decisions and simpler alternatives.
* Clearly state which files will be created or modified.
* After each meaningful code block, explain what it does line by line or section by section.
* Do not hide important logic behind abstractions without first teaching the underlying concept.
* Use beginner-friendly Python, Flask, JavaScript, Bootstrap, SQLAlchemy, Redis, and RQ patterns.
* Avoid generating large amounts of code at once.
* Pause at the end of each phase with:

  1. What we built
  2. How the request flows through the code
  3. How to run and test it
  4. Common errors
  5. A small exercise for me to complete
* Add useful comments, but explain concepts outside the code instead of filling files with excessive comments.
* Update the architecture and learning documentation whenever an important decision changes.

The goal is for me to understand and eventually rebuild the application myself, not simply receive a completed codebase.

make a RULES.md with this and this rule should be followed at all costs.
```

## Prompt 2: Implement Phase 1

Date: 2026-06-27

Purpose:

- Start implementation after the architecture and rules were created.
- Build the smallest working Flask app.
- Mark fully completed phases with a check mark.

Expected output:

- Minimal Flask application.
- Home page.
- Health check route.
- Architecture document updated with completed phase markers.

Original prompt:

```text
Okay let's implement phase - 1 and go forward. whatever phase is fully implemented put ✅ emoji there. okay?
```

## Prompt 3: Implement Phase 2

Date: 2026-06-27

Purpose:

- Add configuration loading before connecting external services.
- Keep real secrets out of source control.
- Record the implementation request for traceability.

Expected output:

- Configuration class.
- Flask app loading config from environment variables.
- Phase 2 smoke test.
- Architecture document updated with completed phase marker.

Original prompt:

```text
lets implement hase 2, record the prompts as well.
```

## Prompt 4: Simplify Phase 2 Config

Date: 2026-06-27

Purpose:

- Correct Phase 2 so it teaches only the configuration needed right now.
- Remove Redis from current config because Redis belongs in the background-jobs phase.
- Keep `DATABASE_URL=sqlite:///dev.db` for the next database phase.
- Keep Groq and ImageKit settings optional until their integration phases begin.

Original prompt:

```text
yes, go ahead
```

Context:

This was approval to fix the earlier mistake where Redis, Groq, and ImageKit settings were introduced too early for the learning flow.

## Prompt 5: Decide Supabase For Database

Date: 2026-06-27

Purpose:

- Evaluate Supabase as the database choice.
- Choose managed Postgres over Firebase/Firestore for the main app database.
- Keep the Flask + SQLAlchemy learning path while avoiding local Postgres setup.

Decision:

- Use Supabase Postgres through `DATABASE_URL`.
- Keep ImageKit as the video storage/transformation system.
- Store app metadata, transcript data, generated clips, and later user ownership in Supabase.

Original prompt:

```text
Instead of using SQLite let's use supabase. Supabase is better than SQLite when you need a complete backend-as-a-service rather than just a local database engine
```

## Prompt 6: Add File Hash And Supabase Phase 3

Date: 2026-06-27

Purpose:

- Make `file_hash` part of the architecture from the first database version.
- Use saved metadata to detect duplicate uploads and avoid repeated AI processing.
- Move Supabase setup into Phase 3.
- Update architecture and prompt traceability.

Original prompt:

```text
we will store filehash as well now not later, update the architecture doc and necassary docs required. we will setup supabase in phase 3 itself. 
```

## Prompt 7: Implement Phase 3 Supabase Postgres

Date: 2026-06-27

Purpose:

- Implement Supabase Postgres as the app database using SQLAlchemy.
- Add the first `Video` model with `file_hash`.
- Prove data can be inserted into and queried from the application database.

Original prompt:

```text
I added the supabase connection string in the env file. Go ahead implemet the phase 3. make sure u follow rules.md. Let me know if you need anything else from me.
```


## Prompt 8: Mark Phase 3 Complete And Explain Phase 4

Date: 2026-06-27

Purpose:

- Mark Phase 3 as complete after Supabase Session Pooler connection worked.
- Keep the architecture document status accurate.
- Explain Phase 4 before implementation, following `RULES.md`.

Original prompt:

```text
session pooler connector worked, can you explain what do we need to do in phase 4 now, phase 3 seems to be working - add a check marked emoji in architecture file (pl keep in mind to do this after every major phase completion). don't implement phase 4, walk me through it first.
```

