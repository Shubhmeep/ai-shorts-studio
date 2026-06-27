# Project Rules

This project is a guided tutorial, not just an implementation task. The goal is for the learner to understand the architecture, rebuild the application independently, and explain the technical decisions clearly.

These rules must be followed for all project work unless they conflict with system, security, tool, or platform instructions. If a conflict exists, the higher-priority instruction wins, and the reason should be explained clearly.

## Working Style

- Build one small, testable step at a time.
- Avoid generating large amounts of code at once.
- Do not write app code before explaining the step.
- Do not hide important logic behind abstractions before teaching the underlying concept.
- Prefer beginner-friendly patterns for Python, Flask, JavaScript, Bootstrap, SQLAlchemy, Redis, and RQ.
- Add useful comments in code, but explain concepts in documentation or conversation instead of filling files with excessive comments.
- Update the architecture and learning documentation whenever an important decision changes.

## Before Writing Code

Before writing or changing code, explain:

- what is being built,
- why it is needed,
- where it fits in the architecture,
- which files will be created or modified,
- important design decisions,
- simpler alternatives and why they are not being used right now.

## After Writing Meaningful Code

After each meaningful code block or small implementation phase, explain the code section by section. The explanation should be beginner-friendly and focus on how the request flows through the code.

## Phase Review Format

At the end of each phase, pause and include:

1. What we built
2. How the request flows through the code
3. How to run and test it
4. Common errors
5. A small exercise for the learner

## Teaching Priorities

- Keep each phase understandable before moving to the next phase.
- Prefer explicit, readable code over clever code.
- Introduce abstractions only after the repeated pattern or complexity is visible.
- Explain external services before integrating them.
- Explain environment variables and secrets before using API keys.
- Treat tests as learning tools, not just correctness checks.

## Project Goal

The AI shorts tool should be built in a way that helps the learner confidently explain the system to recruiters:

- how uploads work,
- how Flask handles API requests,
- why background jobs are needed,
- how Redis and RQ support long-running work,
- how SQLAlchemy stores persistent data,
- how Groq provides transcription and clip selection,
- how ImageKit handles video storage and transformations,
- how the app can grow toward a 50-user deployment.
