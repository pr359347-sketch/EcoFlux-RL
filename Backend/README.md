# 🌱 EcoTwin – Smart Traffic Simulation Backend

> 🚦 An intelligent traffic simulation backend combining **FastAPI, Eclipse SUMO, TraCI, Reinforcement Learning and WebSocket communication** for real-time traffic simulation and monitoring.

---

## 👨‍💻 Member 3 – Backend Development

This branch contains the complete **Backend and Simulation Integration** work developed by **Member 3** for the EcoTwin project.

The backend connects the traffic simulation environment with the application through REST APIs and real-time WebSocket communication.

---

## 🎯 Member 3 Contributions

- ⚡ Developed the FastAPI backend
- 🚦 Integrated Eclipse SUMO with the backend using TraCI
- 🔄 Implemented simulation Start, Step, Stop and Reset operations
- 🤖 Integrated the Reinforcement Learning service
- 📊 Implemented centralized simulation state management
- 🚗 Added real-time vehicle count monitoring
- 🔌 Implemented WebSocket-based live simulation updates
- 🐳 Added Docker support for the backend and SUMO
- 🧪 Tested REST APIs, SUMO, RL integration, WebSocket streaming and Docker execution

---

# 📁 Project Structure

```text
EcoTwin/
│
├── 📂 Backend/
│   │
│   ├── 📂 app/
│   │   │
│   │   ├── 📄 main.py
│   │   │
│   │   ├── 📂 core/
│   │   │   └── ⚙️ Application configuration
│   │   │
│   │   ├── 📂 routes/
│   │   │   ├── 📄 health.py
│   │   │   └── 📄 simulation.py
│   │   │
│   │   ├── 📂 schemas/
│   │   │   └── 📋 API data schemas
│   │   │
│   │   ├── 📂 services/
│   │   │   ├── 🎮 simulation_service.py
│   │   │   └── 🤖 rl_service.py
│   │   │
│   │   ├── 📂 simulation/
│   │   │   ├── 🚦 sumo_client.py
│   │   │   └── 📊 state.py
│   │   │
│   │   └── 📂 websocket/
│   │       └── 🔌 WebSocket management
│   │
│   ├── 🚦 sumo/
│   │   ├── 📄 network.net.xml
│   │   ├── 📄 routes.rou.xml
│   │   └── 📄 simulation.sumocfg
│   │
│   ├── 🧪 tests/
│   │   ├── 📄 test_sumo.py
│   │   └── 📄 test_websocket.py
│   │
│   ├── 🐳 Dockerfile
│   ├── 📦 requirements.txt
│   └── 📖 README.md
│
└── 📂 Other Project Components
