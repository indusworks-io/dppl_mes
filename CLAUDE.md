# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DPPL MES is a Manufacturing Execution System (MES) built on the Frappe framework with a Vue.js frontend. The system tracks manufacturing operations, machines, telemetry data, and provides a real-time factory floor visualization.

## Architecture

### Backend (Python/Frappe)
- **Framework**: Frappe (Python-based ERP framework)
- **App Structure**: Standard Frappe app with modules for Manufacturing and Organization
- **Key DocTypes**:
  - Manufacturing: `Job`, `Job Card`, `Downtime Log`, `Output Log`, `Shift Plan`
  - Organization: `Factory`, `Area`, `Machine`, `Device`, `Operator`, `Telemetry`
- **API Layer**: REST APIs in `dppl_mes/api.py` for telemetry data ingestion and job metrics
- **Real-time**: Socket.IO integration for live data updates

### Frontend (Vue.js)
- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite with custom frappe-ui plugin
- **UI Library**: frappe-ui components + TailwindCSS
- **PWA**: Progressive Web App capabilities with service worker
- **Key Components**:
  - `Home.vue`: Main dashboard with toggle between grid and floor map views
  - `FactoryFloorMap.vue`: Interactive SVG-based factory floor visualization
  - `DashboardComponent.vue`: Grid view of areas and machines
  - `MachineCard.vue`: Individual machine status cards

## Development Commands

### Frontend Development (from `frontend/` directory):
```bash
# Install dependencies
yarn install

# Start development server with hot reload
yarn dev

# Build for production (outputs to ../dppl_mes/public/frontend/)
yarn build

# Code formatting and linting
yarn lint

# Preview production build
yarn preview
```
# Frontend Local Development URL
http://dppl.localhost:8081/frontend/


### Backend Development (from root directory):
```bash
# Install frontend dependencies automatically
npm run postinstall

# Start frontend development
npm run dev

# Build frontend assets
npm run build
```
# Backend Local Development URL
http://dppl.localhost:8000/


### Frappe Commands (from bench directory):
```bash
# Start development server
bench start

# Run migrations
bench migrate

# Install/reinstall app
bench install-app dppl_mes

# Console access
bench console

# Execute tests
bench run-tests dppl_mes
```

## Key File Locations

### Configuration Files
- `hooks.py`: Frappe app configuration and hooks
- `frontend/vite.config.js`: Vite build configuration with frappe-ui integration
- `frontend/biome.json`: Code formatting and linting rules
- `pyproject.toml`: Python project metadata

### Core Backend Files
- `dppl_mes/api.py`: Main API endpoints for telemetry and job metrics
- `dppl_mes/utils.py`: Utility functions
- `dppl_mes/manufacturing/`: Manufacturing-related DocTypes and logic
- `dppl_mes/organization/`: Organization structure DocTypes

### Core Frontend Files
- `frontend/src/main.js`: Vue app entry point
- `frontend/src/App.vue`: Root component
- `frontend/src/pages/Home.vue`: Main dashboard page
- `frontend/src/components/`: Reusable Vue components
- `frontend/src/socket.js`: Socket.IO client setup

## Build Process

1. Frontend builds to `dppl_mes/public/frontend/` directory
2. Entry HTML is copied to `dppl_mes/www/frontend.html` for Frappe integration
3. Assets are served through Frappe's asset management system
4. PWA manifest and service worker are automatically generated

## Data Flow

1. **Telemetry Ingestion**: External devices POST data to `/api/method/dppl_mes.api.create_telemetry`
2. **Real-time Updates**: Socket.IO broadcasts machine status changes to connected clients
3. **Frontend State**: Vue components use frappe-ui's `createListResource` for reactive data fetching
4. **Job Management**: Manufacturing jobs are tracked through Job and Job Card DocTypes

## Frontend Routing

- `/frontend`: Main application entry point (served by `frontend.html`)
- Single Page Application with Vue Router
- Factory floor map accessible via toggle in main dashboard

## Socket.IO Integration

- Client connects to Frappe's built-in Socket.IO server
- Real-time machine status updates
- Automatic reconnection handling
- Used for live dashboard updates without page refresh