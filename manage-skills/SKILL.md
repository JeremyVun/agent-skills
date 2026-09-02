---
name: manage-skills
description: Where skills live and how to create, edit, install or sync them. Use whenever asked to write, add, save, move, update or install a skill, or when a reusable workflow is worth capturing as one.
---

# Manage skills

All skills live in one repository so they can be installed anywhere:

    /Users/jeremy/projects/agent-skills/<skill-name>/SKILL.md

Never create a skill directly under `~/.claude/skills/`, `~/.agents/skills/`
or inside a project.

## Create or edit

1. Write `SKILL.md` with frontmatter `name` (kebab-case, matches the directory)
   and a one-line `description` that says what it does and when to use it.
   Keep the body general: no project names, paths or values that belong in a
   project's own docs.
2. On this machine, expose it with a symlink into the checkout so edits land
   in git, never in an installed copy:
   `ln -s ../../projects/agent-skills/<skill-name> ~/.claude/skills/<skill-name>`
3. Commit and push from `/Users/jeremy/projects/agent-skills`, staging only
   the skill's own directory.

## Install on another machine

The `skills` CLI scans the repo for every `SKILL.md`, so no list is needed:

    npx skills add JeremyVun/agent-skills --all

Scoped to Claude Code, user-level, no prompts:

    npx skills add JeremyVun/agent-skills --skill '*' -a claude-code -g -y

One skill: `--skill <skill-name>`. Installed skills are copies under
`~/.agents/skills/` with symlinks from `~/.claude/skills/`; rerun the command
to update them, and do not edit them in place.
