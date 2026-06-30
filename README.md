# ClipEngine

ClipEngine is a Flask web app for turning long horizontal videos into short vertical clips.

This repository is currently at Phase 0 of implementation.

## Local setup

Create and activate a virtual environment.

Install dependencies with:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in provider credentials when a later phase needs them.

Run the development server with:

```bash
flask --app src.app run
```

Check the health endpoint at:

```text
http://127.0.0.1:5000/health
```
