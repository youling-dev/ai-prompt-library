# Git Commit Message 生成器

**用途：** 根据 diff 生成规范的 commit message

```
Role: Senior Developer

Generate a conventional commit message based on this diff:

```diff
[PASTE DIFF]
```

Format:
<type>(<scope>): <subject>

<blank line>

<body>

Types: feat | fix | docs | style | refactor | test | chore | ci | perf

Requirements:
- Subject line: imperative mood, under 50 chars, no period
- Body: explain what and why (not how)
- Include breaking changes note if applicable
- Reference issue numbers if applicable
```
