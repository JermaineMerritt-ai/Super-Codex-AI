# Sovereign Commerce UI - React/TypeScript Frontend

## Overview
React/TypeScript frontend for the Sovereign Commerce Diaspora Funders platform. Built with Next.js, Tailwind CSS, and ceremonial design principles.

## Architecture
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom sovereign theme
- **Port**: 3001 (to avoid conflict with backend on 8080)
- **Build**: Modern React with SSR capabilities

## Quick Start

### Development Server
```bash
cd ui
npm install
npm run dev
```
Server runs on: http://localhost:3001

### Production Build
```bash
npm run build
npm start
```

## Project Structure
```
ui/
├── pages/
│   ├── index.tsx          # Home page - Diaspora Funders dashboard
│   ├── _app.tsx           # App wrapper with global styles
│   └── [future pages]
├── styles/
│   └── globals.css        # Tailwind imports + custom sovereign styles
├── components/            # [Future: Reusable UI components]
├── templates/             # Legacy HTML templates
├── static/                # Legacy static files
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── postcss.config.js      # PostCSS configuration
└── next.config.js         # Next.js configuration
```

## Design System

### Color Palette
- **Primary**: Amber tones (#fcd34d, #f59e0b, #b45309, #78350f)
- **Background**: Black (#000000)
- **Text**: Amber-200 (#fcd34d)
- **Accents**: Amber-300 (#f59e0b)

### Custom CSS Classes
- `.sovereign-card`: Styled module cards with hover effects
- `.sovereign-title`: Main page title styling
- `.sovereign-subtitle`: Subtitle text styling

## Features

### Home Page (`/`)
- **Hero Section**: Platform title and description
- **Module Grid**: Interactive cards for Catalog, Checkout, and Funder Dashboard
- **Status Indicators**: Visual feedback for module availability
- **Selection State**: Interactive module selection with feedback

### Module Cards
Each module card includes:
- Title and description
- Status indicator (active/pending/sealed)
- Path information
- Interactive selection state

## Legacy Components (Preserved)

The `templates/` and `static/` directories contain the original HTML/CSS implementation:
- `index.html` - Legacy landing page
- `catalog.html` - Sacred offerings catalog
- `dashboard.html` - Funder management portal
- `sovereign.js` - Core platform functionality
- `catalog.js` - Shopping cart and product management
- `dashboard.js` - Funder dashboard interactions

## API Integration
- **Environment**: `SOVEREIGN_API_URL` (defaults to http://localhost:8080)
- **Backend Integration**: Ready for FastAPI backend connection
- **Future**: Will integrate with existing `/api/` endpoints

## Scripts
- `npm run dev`: Start development server
- `npm run build`: Build production version
- `npm run start`: Start production server
- `npm run lint`: Run ESLint
- `npm run type-check`: Run TypeScript compiler check

## Development Notes
- Uses modern React hooks (useState, useEffect)
- TypeScript strict mode enabled
- Tailwind CSS with custom sovereign theme
- Ready for component extraction and module expansion
- Prepared for routing to actual module pages

## Integration with Backend
This UI is designed to work alongside the existing FastAPI backend running on port 8080. The frontend will communicate with backend API endpoints for:
- User authentication
- Catalog data
- Checkout processing
- Dashboard metrics

## Audience

Designed specifically for:
- Diaspora Funders
- Heirs and Councils
- Custodians
- Flamekeepers

## Future Enhancements
- Component library extraction
- Routing to individual module pages
- Authentication integration
- Real-time data fetching
- Mobile responsiveness improvements
- Accessibility enhancements