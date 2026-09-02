---
name: create-skill
description: Where and how to create or edit an agent skill. Use whenever asked to write, add, save, move or update a skill, or when a reusable workflow is worth capturing as one.
---

# Create a skill

All skills live in one repository so they can be installed anywhere:

    /Users/jeremy/projects/agent-skills/<skill-name>/SKILL.md

Never create a skill directly under `~/.claude/skills/`, `~/.agents/skills/`
or inside a project. Steps:

1. Write `SKILL.md` with frontmatter `name` (kebab-case, matches the directory)
   and a one-line `description` that says what it does and when to use it.
   Keep the body general: no project names, paths or values that belong in a
   project's own docs.
2. Expose it locally with a symlink:
   `ln -s ../../projects/agent-skills/<skill-name> ~/.claude/skills/<skill-name>`
3. Commit and push from `/Users/jeremy/projects/agent-skills`, staging only
   the skill's own directory.

Install elsewhere with:

    npx skills add https://github.com/JeremyVun/agent-skills --skill <skill-name>
