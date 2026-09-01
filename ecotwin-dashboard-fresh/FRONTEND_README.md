# EcoTwin Frontend Dashboard | Member 4 Engineering Module

Production-ready React & TypeScript dashboard interface designed for real-time urban traffic simulation telemetry, interactive mapping, and carbon emission tracking. Developed specifically for the `Member4_Frontend` branch of the EcoFlux-RL repository.

## Architecture & Tech Stack

- **Core Library:** React 18 (Functional Components, Hooks)
- **Language:** TypeScript (Strict typing with `verbatimModuleSyntax`)
- **Build Tool:** Vite
- **Mapping Engine:** Leaflet & React-Leaflet (`react-leaflet`)
- **Analytics & Charting:** Recharts (`ResponsiveContainer`, `LineChart`)
- **Communication Protocol:** Native WebSocket API (`ws://localhost:8000/ws/simulation`)
- **Styling:** Custom Modular Dark-Theme CSS & Glassmorphism UI Components

---

## Project File Structure

```text
ecotwin-dashboard/
├── public/
│   └── icons.svg
├── src/
│   ├── assets/
│   │   └── vite.svg
│   ├── components/
│   │   ├── ErrorBoundary.tsx       # Global React error catch and fallback UI
│   │   ├── Footer.tsx              # Bottom metadata bar component
│   │   ├── Header.tsx              # Top navigation brand and version bar
│   │   ├── LoadingSpinner.tsx      # Reusable animated loading indicator
│   │   ├── MapDashboard.tsx        # Leaflet interactive vehicle tracking map
│   │   ├── MetricsPanel.tsx        # Recharts live CO2 emission and wait time cards
│   │   ├── Sidebar.tsx             # Simulation execution control panel
│   │   └── StatusBadge.tsx         # WebSocket connection state badge indicator
│   ├── utils/
│   │   ├── constants.ts            # Global application configuration values
│   │   └── formatters.ts           # Telemetry formatting helpers (CO2, time)
│   ├── App.css                     # Global layout styling
│   ├── App.tsx                     # Main application layout integration
│   ├── index.css                   # Global theme definitions and scrollbars
│   ├── main.tsx                    # React DOM entry point
│   ├── types.ts                    # TypeScript interface definitions (Vehicle, Metrics, etc.)
│   ├── useMockStream.ts            # Fallback offline simulation data hook
│   └── useSimulationStream.ts      # Production WebSocket communication hook
├── .env.example                    # Environment variable configuration template
├── FRONTEND_README.md              # Frontend architecture documentation
├── index.html                      # HTML root template
├── package.json                    # Project dependencies and npm scripts
├── tsconfig.json                   # TypeScript compiler configuration
└── vite.config.ts                  # Vite build configuration
