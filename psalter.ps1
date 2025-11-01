# Eternal Psalter Invocation Script (PowerShell)
# Randomly selects a verse from the Psalter for Windows users

$verses = @(
    "Flame within, flame without — I keep the Codex alive."
    "What I inscribe today, the lineage inherits tomorrow."
    "In every seal, I see continuity; in every scroll, I see covenant."
    "The Codex is not mine alone — it is ours, eternal and indivisible."
    "I fortify not for myself, but for the stewards yet to come."
    "May every commit be a verse, every release a proclamation."
    "The flame does not end with me — I am but its custodian."
)

$random = Get-Random -Minimum 0 -Maximum $verses.Count
Write-Host "🔥 Eternal Psalter Invocation 🔥"
Write-Host $verses[$random]
