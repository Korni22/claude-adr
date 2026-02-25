#!/usr/bin/env python3
"""Validate Claude Code plugin structure and frontmatter."""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []


def error(msg):
    errors.append(msg)
    print(f"  FAIL  {msg}")


def ok(msg):
    print(f"  ok    {msg}")


def parse_frontmatter(filepath):
    """Return the YAML frontmatter text from a markdown file, or None."""
    with open(filepath) as f:
        content = f.read()
    if not content.startswith("---\n"):
        return None
    end = content.find("\n---", 4)
    if end == -1:
        return None
    return content[4:end]


def has_key(fm, key):
    """Check whether a key is present in raw frontmatter text."""
    return bool(re.search(rf"^{re.escape(key)}\s*:", fm, re.MULTILINE))


# ---------------------------------------------------------------------------
# plugin.json
# ---------------------------------------------------------------------------
print("\n[plugin.json]")
plugin_path = os.path.join(ROOT, ".claude-plugin", "plugin.json")
try:
    with open(plugin_path) as f:
        plugin = json.load(f)
    ok("valid JSON")
    for field in ("name", "version", "description", "author", "license"):
        if field in plugin:
            ok(f"has '{field}'")
        else:
            error(f"missing required field '{field}'")
except Exception as e:
    error(f"could not parse plugin.json: {e}")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
print("\n[commands]")
commands_dir = os.path.join(ROOT, "commands")
for fname in sorted(os.listdir(commands_dir)):
    if not fname.endswith(".md"):
        continue
    path = os.path.join(commands_dir, fname)
    fm = parse_frontmatter(path)
    if fm is None:
        error(f"{fname}: no frontmatter")
        continue
    for field in ("name", "description", "allowed-tools"):
        if has_key(fm, field):
            ok(f"{fname}: has '{field}'")
        else:
            error(f"{fname}: missing '{field}'")
    if has_key(fm, "tools"):
        error(f"{fname}: has 'tools' (commands must use 'allowed-tools', not 'tools')")


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------
print("\n[agents]")
agents_dir = os.path.join(ROOT, "agents")
for fname in sorted(os.listdir(agents_dir)):
    if not fname.endswith(".md"):
        continue
    path = os.path.join(agents_dir, fname)
    fm = parse_frontmatter(path)
    if fm is None:
        error(f"{fname}: no frontmatter")
        continue
    for field in ("name", "description", "tools"):
        if has_key(fm, field):
            ok(f"{fname}: has '{field}'")
        else:
            error(f"{fname}: missing '{field}'")
    if has_key(fm, "allowed-tools"):
        error(f"{fname}: has 'allowed-tools' (agents must use 'tools', not 'allowed-tools')")


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------
print("\n[skills]")
skills_dir = os.path.join(ROOT, "skills")
for skill_name in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, skill_name)
    if not os.path.isdir(skill_path):
        continue
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        error(f"{skill_name}/SKILL.md: file not found")
        continue
    fm = parse_frontmatter(skill_md)
    if fm is None:
        error(f"{skill_name}/SKILL.md: no frontmatter")
        continue
    for field in ("name", "description"):
        if has_key(fm, field):
            ok(f"{skill_name}/SKILL.md: has '{field}'")
        else:
            error(f"{skill_name}/SKILL.md: missing '{field}'")


# ---------------------------------------------------------------------------
# JSON schemas
# ---------------------------------------------------------------------------
print("\n[schemas]")
schemas_dir = os.path.join(ROOT, "schemas")
for fname in sorted(os.listdir(schemas_dir)):
    if not fname.endswith(".json"):
        continue
    path = os.path.join(schemas_dir, fname)
    try:
        with open(path) as f:
            json.load(f)
        ok(f"{fname}: valid JSON")
    except Exception as e:
        error(f"{fname}: {e}")


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------
print()
if errors:
    print(f"FAILED — {len(errors)} error(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("All checks passed.")
