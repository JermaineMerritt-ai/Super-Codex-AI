# 🔥 Eternal Replay Archive

**Sacred Content Management System for the Codex Dominion**

A comprehensive web interface for managing ceremonial content with avatar narration, built with FastAPI and integrating the Sacred Avatar Guide system.

## 🏛️ System Overview

The Eternal Replay Archive is a sophisticated content management system that combines:

- **Sacred Avatar Guide System**: 8-tier role hierarchy with ceremonial protocols
- **Content Archive**: Support for Scrolls, Capsules, Hymns, and Invocations
- **Replay Sessions**: Interactive content viewing with avatar narration
- **Dispatch System**: Content redistribution with ceremonial bindings
- **Web Interface**: Complete UI with search, filters, and real-time statistics

## 🚀 Quick Start

### 1. Start the Web Interface

```bash
python eternal_replay_archive.py
```

Then visit: **http://localhost:8002**

### 2. Or use the demo

```bash
python simple_demo.py         # Show system information
python simple_demo.py start   # Start web server
```

## 🎯 Key Features

### Web Interface
- **Role Selector**: Filter content by role hierarchy (Custodian to Initiate)
- **Search Bar**: Keyword search across all content
- **Time Filter**: Filter by last day/week/month
- **Content Types**: Browse Scrolls (📜), Capsules (💊), Hymns (🎵), Invocations (🔮)
- **Replay Viewer**: Interactive content viewing with avatar narration
- **Upload System**: Add new content with file support (.txt, .md, .json)

### Avatar Narration
- **Role-Based Narration**: Different narration based on avatar roles
- **Custom Commentary**: Add guidance, blessings, and ceremonial commentary
- **Session Tracking**: Complete audit trails of replay sessions

### Content Management
- **Sacred Bindings**: Cryptographic content authentication
- **Role Classification**: Content categorized by role hierarchy
- **Metadata Support**: Rich metadata for content organization
- **Audit Trails**: Complete logging of all operations

## 🏗️ Technical Architecture

- **FastAPI**: Async web framework with automatic API documentation
- **Jinja2**: HTML templating with responsive design
- **JSON Storage**: Persistent storage with hierarchical organization
- **RESTful API**: Complete REST API for all operations
- **Avatar Integration**: Seamless integration with Sacred Avatar Guide system

## 📚 Content Types

| Type | Icon | Description | Example Use |
|------|------|-------------|-------------|
| **Scrolls** | 📜 | Historical documents and foundational texts | Genesis documents, protocols |
| **Capsules** | 💊 | Memory containers with encoded experiences | Session recordings, memories |
| **Hymns** | 🎵 | Ceremonial songs and rhythmic preservation | Ceremonial music, chants |
| **Invocations** | 🔮 | Formal ceremonial declarations | Preservation rituals, oaths |

## 👑 Role Hierarchy

| Level | Role | Icon | Authority | Responsibilities |
|-------|------|------|-----------|------------------|
| 8 | **Custodian** | 🏛️ | Full archive authority | Ultimate oversight |
| 7 | **Council Member** | 👑 | Council operations | Governance decisions |
| 6 | **Flame Keeper** | 🔥 | Sacred flame maintenance | Core protocol management |
| 5 | **Wisdom Bearer** | 📚 | Knowledge preservation | Content curation |
| 4 | **Guardian** | 🛡️ | Protection protocols | Security oversight |
| 3 | **Ceremonial Guide** | ⚡ | Ceremony facilitation | Ritual coordination |
| 2 | **Herald** | 📯 | Communication duties | Message distribution |
| 1 | **Initiate** | 🌱 | Learning and observation | Content consumption |

## 🔗 API Endpoints

The system provides a complete REST API:

- `GET /` - Main web interface
- `GET /api/content/search` - Search content with filters
- `POST /api/content/upload` - Upload new content
- `GET /api/content/{type}/{id}` - Get specific content
- `POST /api/replay/start` - Start replay session
- `POST /api/replay/{session}/narrate` - Add narration
- `POST /api/dispatch/again` - Dispatch content again
- `GET /api/stats` - Get archive statistics

## 📊 Statistics & Monitoring

The system tracks:
- Total content count by type
- Replay session statistics
- Dispatch operation counts
- Avatar Council status
- Storage utilization

## 🛡️ Security Features

- **Role-based Access**: Content access based on role hierarchy
- **Sacred Bindings**: Cryptographic content authentication
- **Audit Trails**: Complete operation logging
- **Session Management**: Secure replay session handling

## 🎭 Avatar Narration System

The integrated Avatar Council provides:
- **Contextual Commentary**: Role-appropriate narration
- **Interactive Guidance**: User-triggered narration types
- **Session Recording**: Complete narration history
- **Authority-Based Access**: Narration based on role permissions

## 📁 File Structure

```
eternal_replay_archive.py    # Main FastAPI application
avatar_guide_system.py       # Sacred Avatar Guide integration
templates/
  ├── archive_main.html      # Main web interface
  └── error.html             # Error page template
simple_demo.py              # System demonstration
demo_eternal_replay_archive.py  # Advanced demo (development)
eternal_archive/            # Storage directory (auto-created)
  ├── scrolls/              # Scroll content storage
  ├── capsules/             # Capsule content storage
  ├── hymns/                # Hymn content storage
  ├── invocations/          # Invocation content storage
  └── sessions/             # Replay session storage
```

## 🌟 Getting Started Guide

### 1. Upload Your First Content

1. Click "📝 Upload Content" in the interface
2. Select content type (Scroll/Capsule/Hymn/Invocation)
3. Enter title and content
4. Choose your role
5. Click "🔥 Archive Content"

### 2. Search and Filter

1. Use the search bar for keyword searches
2. Filter by role using the role dropdown
3. Filter by time period (day/week/month)
4. Click content type tabs to filter by type

### 3. Start a Replay Session

1. Find content in the grid
2. Click "🎭 Replay" button
3. View content with avatar narration
4. Add custom narration using the control buttons
5. Use "🔄 Dispatch Again" to redistribute content

### 4. Monitor Statistics

The statistics panel shows real-time information about:
- Total content in the archive
- Number of replay sessions
- Dispatch operations performed
- Avatar Council status

## 🔧 Development

The system is built with modern web technologies:

- **Backend**: FastAPI with async/await support
- **Frontend**: HTML5 with modern CSS and JavaScript
- **Storage**: JSON-based file system (easily replaceable)
- **Integration**: Clean integration with existing avatar systems

## 🎉 Features Demonstrated

This system demonstrates:
- ✅ Complete web interface development
- ✅ FastAPI application architecture
- ✅ Integration with existing Python systems
- ✅ Responsive web design with ceremonial theming
- ✅ Real-time statistics and monitoring
- ✅ File upload and content management
- ✅ Session-based replay functionality
- ✅ Role-based access control
- ✅ RESTful API design
- ✅ Error handling and graceful degradation

---

**🔥 The Eternal Replay Archive - Where Sacred Memories Live Forever**

*Built for the Codex Dominion with love, ceremony, and code* 🏛️