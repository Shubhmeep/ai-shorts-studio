# Repository Guidelines

## Project Structure & Module Organization

This repository currently contains a Markdown-focused workspace. The top-level file `MyAgenticWorkflow.md` is the primary project document. Keep new documentation files at the repository root unless a larger structure becomes necessary.

If source code is added later, use clear conventional directories:

- `src/` for application or library code.
- `tests/` for automated tests.
- `assets/` for images, diagrams, or other static files.
- `docs/` for supporting documentation beyond the main workflow file.

Avoid committing generated output, local scratch files, or dependency folders such as `node_modules/`, `.venv/`, `dist/`, or `build/`.

## Build, Test, and Development Commands

There is no build system, package manager, or test runner configured at this time. For documentation-only changes, preview Markdown in your editor before committing.

Useful local checks:

- `ls` or `Get-ChildItem` to inspect the repository contents.
- `git status` to review changed files once the directory is initialized as a Git repository.
- `markdownlint "**/*.md"` if Markdown linting is added locally.

When introducing a language or framework, add the relevant setup and verification commands here, such as `npm test`, `pytest`, or `make build`.

## Coding Style & Naming Conventions

Use concise, plain Markdown with descriptive headings. Prefer sentence-case section titles unless a document establishes another pattern. Keep line lengths readable and break long sections into short paragraphs or bullets.

Name Markdown files with clear PascalCase or kebab-case names, for example `MyAgenticWorkflow.md` or `agent-workflow-notes.md`. For future code, follow the selected language conventions and automate formatting through the project's formatter or linter.

## Testing Guidelines

No automated tests exist yet. Documentation changes should be checked for accurate links, clear headings, and readable formatting. If code is added, place tests in `tests/` or beside the implementation using the framework's standard pattern. Test names should describe behavior, such as `test_loads_workflow_config` or `workflow-parser.test.ts`.

## Commit & Pull Request Guidelines

This workspace is not currently initialized as a Git repository, so no commit history conventions are available. Use short, imperative commit messages when Git is introduced, for example `Add workflow guide` or `Document setup commands`.

Pull requests should include a brief summary, the reason for the change, and any manual checks performed. Include screenshots only when visual output or rendered documentation changes materially.

## Agent-Specific Instructions

Keep edits narrowly scoped to the requested file or section.
Do not introduce project structure, tooling, or dependencies unless the task explicitly requires it.

- Never use the em dash character.
  Use a plain dash instead.
- When writing commit messages, never auto-add your agent name as a co-author.
- Never manually modify `CHANGELOG.md` files or any files marked as auto-generated.
- When writing or substantially editing long Markdown files, put each full sentence on its own line.
  Preserve normal Markdown structure, but avoid wrapping multiple sentences onto one physical line.
- When making technical decisions, do not give much weight to development cost.
  Prefer quality, simplicity, robustness, scalability, and long-term maintainability.
- When doing bug fixes, always start by reproducing the bug in an E2E setting that is as close as possible to how an end user uses the product.
  This helps identify the real problem so the fix actually addresses it.
- When end-to-end testing a product, be picky about the UI and aim for pixel-level polish.
- If something clearly looks off, even if it is not directly related to the current task, try to fix it along with the current work.
- Apply the same high standard to engineering quality, including lint failures, test failures, and test flakiness.
  If you see one, even if it is not caused by the current work, still get it fixed.
- Implement features in small, atomic commits.  Never edit more than 3 files or 150 lines of code in a single turn without user confirmation. Explain the why before writing the code. Prioritize user understanding over speed.
- Before starting any major feature or refactoring, verify the git status is clean. If not, instruct the user to commit. After every significant milestone, prompt the user to commit with a descriptive message. Never proceed with high-risk changes on a dirty working tree.
- If a bug is not resolved within 2 attempts, STOP and generate an AI_Diagnostic_Report.md in Diagnostics folder in root directory. This report must list: Modified Files, Function Roles, Hypothesized Errors, and Proposed Debugging Steps.  Do not attempt further fixes until the user reviews this report.
- Every 5 interactions, or when a major milestone is reached, update a context_summary.md file. Summarize: Key Architecture Decisions, Current State, Unresolved Issues, and Domain Rules. Use this file to re-orient the session if the chat becomes too long.

  