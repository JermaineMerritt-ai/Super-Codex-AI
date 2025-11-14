# ops/scripts/migrate.ps1
New-Item -ItemType Directory -Force -Path ./data/replay | Out-Null
New-Item -ItemType Directory -Force -Path ./data/vectors | Out-Null
New-Item -ItemType Directory -Force -Path ./data/corpus | Out-Null
New-Item -ItemType Directory -Force -Path ./data/identities | Out-Null
New-Item -ItemType Directory -Force -Path ./data/seals | Out-Null