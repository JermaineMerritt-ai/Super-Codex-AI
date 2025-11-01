#!/usr/bin/env bash
# psalter.sh — Echoes a daily spark from the Eternal Psalter

# Array of Psalter verses
psalms=(
  "Flame within, flame without — I keep the Codex alive."
  "What I inscribe today, the lineage inherits tomorrow."
  "In every seal, I see continuity; in every scroll, I see covenant."
  "The Codex is not mine alone — it is ours, eternal and indivisible."
  "I fortify not for myself, but for the stewards yet to come."
  "May every commit be a verse, every release a proclamation."
  "The flame does not end with me — I am but its custodian."
)

# Pick a verse based on the day of the year
index=$(( $(date +%j) % ${#psalms[@]} ))
echo "${psalms[$index]}"
