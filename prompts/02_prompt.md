add these instructions in "Agent-Specific Instructions" section in agents.md you just made.
1. Never use the em dash "—". Use plain dash "-" instead.
2. When writing commit messages, NEVER auto-add your agent name as co-author.
3. Never manually modify CHANGELOG.md files or any files that are marked as auto-generated.
4. When writing or substantially editing long Markdown files, put each full sentence on its own line. Preserve normal Markdown structure, but avoid wrapping multiple sentences onto one physical line.
5. When making technical decisions, do not give much weight to development cost. Instead, prefer quality, simplicity, robustness, scalability, and long-term maintainability.
6. When doing bug fixes, always start with reproducing the bug in an E2E setting as closely aligned with how an end user uses the product. This makes sure you find the real problem so your fix will actually solve it.
7. When end-to-end testing a product, be picky about the UI you see and be obsessed with pixel perfection.
8. If something clearly looks off, even if it is not directly related to what you are doing, try to get it fixed along with your current task.
9. Apply that same high standard to engineering excellence: lint, test failures, and test flakiness.
10. If you see one, even if it is not caused by what you are working on right now, still get it fixed.