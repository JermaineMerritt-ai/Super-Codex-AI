# ops/scripts/ingest.ps1
param([string]$CorpusPath = "./data/corpus")

Write-Host "🔥 Six Engines RAG Corpus Ingestion" -ForegroundColor Yellow
Write-Host "📁 Corpus Path: $CorpusPath" -ForegroundColor Cyan

python test_rag_direct.py "$CorpusPath"