# Codex Capsule Viewer

> Sacred knowledge preserved in temporal capsules - A sovereign viewing interface

## Overview

The Codex Capsule Viewer is a ceremonial application designed to access and interact with knowledge capsules within the sovereign codex system. It provides a comprehensive interface for viewing capsule contents, validating heir recognition, and replaying covenant seal histories.

## Features

### 🔮 **Core Modules**
- **Capsule List**: Grid view of available knowledge capsules with sigils and summaries
- **Capsule Detail**: Detailed view of individual capsule content and metadata
- **Heir Recognition**: Access control system validating user permissions against capsule heir rights
- **Covenant Replay**: Historical event replay system showing capsule covenant seal progression

### 🎨 **Dual Themes**
- **Dark Constellation**: Dark stellar theme with amber accents representing the vast codex cosmos
- **Amber Flame**: Warm flame theme with amber and gold tones representing ceremonial fire

### 🛡️ **Ceremonial Security**
- Heir-based role validation (custodian, flamekeeper, council)
- Covenant seal verification and integrity checking
- Genesis, authority, honor, ritual, and legacy seal support

## Quick Start

### Backend (FastAPI)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python services/main.py
# or
uvicorn services.main:app --host 127.0.0.1 --port 8080 --reload
```

### Frontend (React)
```bash
# Serve the static UI (no build required)
python -m http.server 3000 --directory ui

# Or use Node.js
cd ui && npx serve .
```

### Access the Application
- **API**: http://127.0.0.1:8080
- **UI**: http://localhost:3000
- **API Docs**: http://127.0.0.1:8080/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/capsules` | List all available capsules |
| GET | `/api/capsules/{id}` | Get detailed capsule information |
| POST | `/api/capsules` | Create a new capsule |
| GET | `/health` | API health check |

## Data Models

### Capsule
```json
{
  "id": "string",
  "title": "string", 
  "sigil": "string",
  "createdAt": "datetime",
  "content": "string | null",
  "heirRights": ["custodian", "flamekeeper"],
  "covenantSeals": ["genesis", "authority", "honor"]
}
```

### CapsuleResponse (List View)
```json
{
  "id": "string",
  "title": "string",
  "sigil": "string",
  "createdAt": "datetime", 
  "summary": "string | null"
}
```

## Theme Configuration

The application supports dynamic theme switching between two ceremonial themes:

```javascript
// Dark Constellation Theme
{
  "primary": "#f59e0b",
  "background": "#0f172a",
  "surface": "#1e293b",
  "text": "#fef3c7"
}

// Amber Flame Theme  
{
  "primary": "#b45309",
  "background": "#fef7cd",
  "surface": "#fde68a", 
  "text": "#1f2937"
}
```

## Ceremonial Features

### Heir Recognition
- Validates user roles against capsule heir rights
- Supports custodian, flamekeeper, and council permissions
- Provides visual feedback for access status

### Covenant Replay
- Displays chronological event timeline for each capsule
- Shows seal application history and integrity verification
- Animated replay functionality with progress tracking

## Development

### Project Structure
```
codex-capsule-viewer/
├── services/
│   └── main.py          # FastAPI backend
├── models/
│   └── capsule.py       # Pydantic data models
├── ui/
│   ├── index.html       # Main application
│   ├── App.jsx          # Root React component
│   └── components/
│       ├── capsule-list.jsx
│       ├── capsule-detail.jsx
│       ├── heir-recognition.jsx
│       └── covenant-replay.jsx
├── package.json         # Dependencies and scripts
├── requirements.txt     # Python dependencies  
└── manifest.json        # Application manifest
```

### Technology Stack
- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: React 18, TailwindCSS, Babel Standalone
- **Styling**: Custom ceremonial themes with CSS animations
- **Data**: In-memory storage (easily replaceable with database)

## Deployment

The application is designed for both local development and production deployment:

```bash
# Development mode with hot reload
npm run dev

# Production mode
npm start

# Static file serving
npm run serve
```

## License

Sovereign-License-1.0 - Sacred knowledge under ceremonial governance

## Contributing

Contributions welcome under the sovereign codex protocols. Please ensure all submissions maintain ceremonial standards and heir recognition compatibility.

---

*Crafted with reverence for the eternal codex* ⚡🔥⚖️