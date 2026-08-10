# EcoFlux-RL
Reinforcement Learning for Urban Carbon-Aware Traffic Signal Optimization
# 🌱 EcoFlux-RL

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge" alt="Project Status"/>
  <img src="https://img.shields.io/badge/AI-Reinforcement%20Learning-blueviolet?style=for-the-badge" alt="AI"/>
  <img src="https://img.shields.io/badge/Simulation-SUMO-orange?style=for-the-badge" alt="SUMO"/>
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge" alt="React"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

<h3 align="center">
  Reinforcement Learning for Urban Carbon-Aware Traffic Signal Optimization
</h3>

<p align="center">
  🚦 Smarter Traffic &nbsp; • &nbsp; 🌱 Cleaner Air &nbsp; • &nbsp; 🏙️ Better Cities
</p>

---

## 🚧 Project Status

> **EcoFlux-RL is currently under active development.**

The project is being developed as a **3-week, 4-member collaborative system** combining:

- 🚗 Urban traffic simulation
- 🤖 Reinforcement Learning
- 🌫️ Carbon emission monitoring
- 🚦 Dynamic traffic signal control
- ⚡ Real-time API streaming
- 🗺️ Interactive city dashboard

The final goal is to build a working simulation in which a **PPO-based Reinforcement Learning agent dynamically controls traffic lights** while balancing **vehicle waiting time and localized CO₂ buildup**.

---

## 🌍 About The Project

Traditional traffic signal optimization systems primarily focus on reducing vehicle waiting time and improving traffic flow.

However, traffic optimization decisions can also affect the concentration of pollution around busy intersections.

**EcoFlux-RL** addresses this problem by introducing an environmental objective into traffic signal optimization.

The system creates a simulated city using **SUMO (Simulation of Urban MObility)** and uses a **Reinforcement Learning agent based on PPO** to dynamically control traffic-light phases.

The agent is trained to balance:

```text
🚗 Traffic Efficiency
        +
🌫️ Environmental Impact
        ↓
🌱 Sustainable Urban Mobility
```

---

# 🎯 Problem Statement

Urban traffic optimization algorithms are commonly designed to minimize:

- Vehicle waiting time
- Traffic congestion
- Vehicle delays

But these approaches may not explicitly consider localized environmental impact.

This can allow:

```text
Heavy Traffic
     ↓
Long Vehicle Queues
     ↓
Higher Emissions
     ↓
Localized CO₂ / Pollution Buildup
```

### EcoFlux-RL aims to solve this by:

```text
Traffic Optimization
        +
Carbon-Aware Optimization
        ↓
Dynamic Traffic Signal Control
        ↓
Cleaner & More Efficient Urban Mobility
```

---

# 💡 Our Solution

EcoFlux-RL combines **Simulation + Reinforcement Learning + Backend + Visualization** into one complete system.

### Core idea:

> Instead of asking only **"How can we move vehicles faster?"**,  
> EcoFlux-RL also asks **"How can we move vehicles efficiently while reducing localized pollution?"**

---

# 🧠 System Architecture

```text
                    ┌─────────────────────────┐
                    │     SUMO Simulation     │
                    │    Urban Traffic Grid   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      TraCI Interface    │
                    │ Traffic + Emission Data │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Gym Environment      │
                    │ State + Action + Reward │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       PPO Agent         │
                    │ Reinforcement Learning  │
                    └────────────┬────────────┘
                                 │
                         Traffic Actions
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    │    REST + WebSockets    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    React Dashboard      │
                    │ Traffic + CO₂ Heatmap   │
                    └─────────────────────────┘
```

---

# 🔄 Complete System Workflow

```text
1. SUMO generates traffic
             ↓
2. TraCI collects simulation state
             ↓
3. Gym environment processes the state
             ↓
4. PPO agent observes the environment
             ↓
5. PPO selects traffic-light action
             ↓
6. SUMO applies the selected action
             ↓
7. Traffic + emission state changes
             ↓
8. FastAPI receives simulation state
             ↓
9. WebSocket streams live data
             ↓
10. React dashboard visualizes the city
             ↓
11. Metrics and pollution heatmap update
```

---

# ✨ Key Features

## 🚗 1. Urban Traffic Simulation

The system uses **SUMO** to simulate:

- Roads
- Intersections
- Traffic lights
- Vehicles
- Vehicle movement
- Traffic demand
- Emission-related data

---

## 🌫️ 2. Carbon / Emission Monitoring

The simulation collects environmental and traffic information such as:

- CO₂ emissions
- Vehicle positions
- Traffic density
- Waiting time
- Traffic-light phases

This information is used by the RL environment and dashboard.

---

## 🤖 3. Reinforcement Learning

A **PPO (Proximal Policy Optimization)** agent is used to learn traffic signal control.

The agent receives the current environment state and selects an action for the traffic lights.

```text
Environment State
       ↓
PPO Agent
       ↓
Traffic-Light Action
       ↓
SUMO
       ↓
New Environment State
       ↓
Reward
       ↓
Learning
```

---

## 🎯 4. Multi-Objective Reward

The project does not focus only on traffic flow.

The reward function is designed to consider both:

### Traffic objective

Reduce:

- Vehicle waiting time
- Traffic delay
- Congestion

### Environmental objective

Reduce:

- CO₂ emissions
- Localized pollution buildup

Conceptually:

```text
Reward
   =
Traffic Efficiency
   +
Environmental Health
```

The reward weights will be tuned during development.

---

## 🚦 5. Dynamic Traffic Signal Control

Instead of using only fixed traffic-light timers, the trained RL agent will dynamically determine traffic-light actions based on the current simulated state.

```text
Current Traffic
      +
Current Emissions
      +
Vehicle Waiting
      ↓
   PPO Agent
      ↓
Traffic-Light Decision
```

---

## ⚡ 6. Real-Time Data Streaming

The backend will use:

- FastAPI
- WebSockets

to stream simulation data to the frontend.

Example streamed data:

```json
{
  "timestamp": 125,
  "vehicles": [],
  "traffic_lights": [],
  "co2_levels": [],
  "average_wait_time": 0,
  "simulation_status": "running"
}
```

> The exact production schema will be finalized during integration between the Backend and Frontend teams.

---

# 🗺️ Cityscape Dashboard

The final dashboard will provide an interactive view of the simulated city.

### Planned visualization:

```text
┌──────────────────────────────────────────────────────────┐
│                    ECOFLUX-RL DASHBOARD                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   🌫️ CO₂ HEATMAP              🚦 TRAFFIC LIGHTS         │
│                                                          │
│      🔴 High pollution          🟢 Green                 │
│      🟠 Medium                  🟡 Yellow                │
│      🟢 Low                     🔴 Red                   │
│                                                          │
│          🚗  🚗         🚙                               │
│             🚕      🚗                                  │
│                                                          │
├───────────────────────┬──────────────────────────────────┤
│ Live Metrics          │ Performance                       │
│                       │                                  │
│ Avg. Wait Time        │ Reward                           │
│ Total CO₂             │ CO₂ Trend                        │
│ Vehicle Count         │ Waiting Time                     │
│ Throughput            │                                  │
└───────────────────────┴──────────────────────────────────┘
```

### Dashboard components

- 🗺️ Interactive city map
- 🚗 Live vehicle positions
- 🌫️ Carbon heatmap
- 🚦 Traffic-light states
- 📊 Average waiting time
- 📈 CO₂ metrics
- 🎮 Simulation controls
- 📉 RL performance charts

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Programming | Python |
| Traffic Simulation | SUMO |
| Simulation Interface | TraCI |
| RL Environment | OpenAI Gym |
| RL Framework | Ray RLlib |
| RL Algorithm | PPO |
| Backend | FastAPI |
| Real-Time Communication | WebSockets |
| Frontend | React |
| Frontend Language | TypeScript |
| Maps | Deck.gl / Leaflet |
| Charts | Chart.js / Recharts |
| Containerization | Docker |
| Version Control | Git + GitHub |

---

# 📁 Project Structure

```text
EcoFlux-RL/
│
├── simulation/
│   ├── configs/
│   ├── networks/
│   ├── routes/
│   ├── emissions/
│   └── run_simulation.py
│
├── rl/
│   ├── environment/
│   ├── agents/
│   ├── training/
│   └── evaluation/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── websocket/
│   │   ├── services/
│   │   └── schemas/
│   │
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── map/
│   │   ├── charts/
│   │   └── services/
│   │
│   └── package.json
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── rl_design.md
│
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# 👥 Team Structure

The project is divided into four parallel development tracks.

| Member | Role | Main Technologies |
|---|---|---|
| 👤 Member 1 | Simulation Engineer | SUMO, Python, TraCI |
| 🤖 Member 2 | RL / ML Engineer | Gym, Ray RLlib, PPO |
| ⚙️ Member 3 | Backend / API Engineer | FastAPI, WebSockets, Docker |
| 🎨 Member 4 | Frontend Dashboard Engineer | React, Deck.gl / Leaflet, Charts |

---

# 📅 3-Week Development Roadmap

## 🟢 WEEK 1 — FOUNDATION

### 👤 Member 1 — Simulation

- Install and configure SUMO
- Create mock city grid
- Create intersections and roads
- Configure traffic lights
- Generate traffic demand
- Run headless simulation
- Log vehicle positions

### 🤖 Member 2 — RL / ML

- Design Gym environment
- Define observation space
- Define action space
- Design multi-objective reward function
- Setup Ray RLlib
- Create PPO training structure
- Run random-action smoke test

### ⚙️ Member 3 — Backend

- Scaffold FastAPI server
- Create REST endpoints
- Create simulation start/stop endpoints
- Setup WebSocket
- Test mock live data
- Define JSON streaming schema

### 🎨 Member 4 — Frontend

- Create React application
- Setup project structure
- Integrate map library
- Render city grid
- Create dashboard layout
- Add simulation controls
- Add placeholder metrics

### ✅ Week 1 Goal

```text
SUMO Grid       → Working
Gym Skeleton    → Working
FastAPI Server  → Working
React Map       → Working
Data Contract   → Agreed
```

---

# 🟡 WEEK 2 — INTEGRATION

### 👤 Member 1 — Simulation

- Wrap SUMO using TraCI
- Add emission output
- Collect CO₂ data
- Expose simulation state
- Validate timestep data

### 🤖 Member 2 — RL / ML

- Connect SUMO environment
- Train baseline PPO agent
- Log training metrics
- Monitor reward progression
- Measure waiting time
- Measure CO₂
- Compare with fixed-timer baseline

### ⚙️ Member 3 — Backend

- Connect simulation to WebSocket
- Stream live simulation state
- Implement throttling
- Add session management
- Add simulation reset/start/stop
- Validate continuous data streaming

### 🎨 Member 4 — Frontend

- Connect WebSocket
- Render live vehicles
- Add carbon heatmap
- Update map continuously
- Handle real-time state updates
- Optimize rendering performance

### ✅ Week 2 Goal

```text
SUMO
  ↓
TraCI
  ↓
Backend
  ↓
WebSocket
  ↓
React Dashboard
```

At the same time:

```text
SUMO + Gym
     ↓
Baseline PPO
     ↓
Training Progress
```

---

# 🔵 WEEK 3 — OPTIMIZATION & FINAL INTEGRATION

### 👤 Member 1 — Simulation

- Optimize simulation performance
- Support RL integration
- Fix state/data mismatches
- Prepare final demo scenario

### 🤖 Member 2 — RL / ML

- Tune PPO hyperparameters
- Tune reward weights
- Train final agent
- Evaluate agent
- Export final checkpoint
- Create lightweight inference function
- Document final performance

### ⚙️ Member 3 — Backend

- Integrate trained RL agent
- Connect RL decisions to SUMO
- Optimize inference latency
- Optimize WebSocket broadcasting
- Dockerize backend
- Perform final integration testing

### 🎨 Member 4 — Frontend

- Add live metric charts
- Add CO₂ visualization
- Add average waiting time chart
- Improve heatmap
- Add legends
- Improve UI/UX
- Responsive dashboard
- Final demo preparation

### 🏆 Week 3 Goal

```text
              ┌─────────────┐
              │ SUMO Traffic│
              └──────┬──────┘
                     ↓
              ┌─────────────┐
              │ RL / PPO    │
              └──────┬──────┘
                     ↓
           Dynamic Traffic Lights
                     ↓
              ┌─────────────┐
              │  FastAPI    │
              │ WebSocket   │
              └──────┬──────┘
                     ↓
              ┌─────────────┐
              │    React    │
              │  Dashboard  │
              └─────────────┘
```

---

# 📊 Evaluation Metrics

The project will evaluate the system using three major categories.

## 🚗 Traffic Metrics

- Average waiting time
- Vehicle delay
- Queue length
- Traffic throughput

## 🌱 Environmental Metrics

- Total CO₂ emissions
- Average CO₂ emissions
- Localized pollution concentration
- Emission reduction

## 🤖 Reinforcement Learning Metrics

- Episode reward
- Reward progression
- PPO performance
- Training stability
- Baseline comparison

---

# ⚖️ Baseline Comparison

The trained RL agent will be compared against a traditional fixed-timer traffic-light strategy.

```text
                Traffic Control
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
   Fixed-Timer              PPO Agent
    Baseline                EcoFlux-RL
          │                       │
          └───────────┬───────────┘
                      ↓
              Compare Metrics
                      ↓
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
   Wait Time         CO₂        Throughput
```

The objective is to demonstrate measurable improvement across the selected traffic and environmental metrics.

---

# 🔌 Backend API Design

The backend will act as the bridge between the simulation/RL layer and the frontend.

### Planned REST endpoints

```text
POST   /simulation/start
POST   /simulation/stop
POST   /simulation/reset
GET    /simulation/status
```

### Planned WebSocket

```text
WS /ws/simulation
```

The WebSocket will stream:

```text
Vehicle Positions
Traffic-Light States
CO₂ Levels
Waiting Time
Simulation Status
```

> API paths and payloads may evolve during implementation.

---

# 🌐 Frontend Architecture

```text
React Application
       │
       ├── Dashboard
       │
       ├── City Map
       │     ├── Vehicles
       │     ├── Roads
       │     ├── Traffic Lights
       │     └── CO₂ Heatmap
       │
       ├── Metrics
       │     ├── CO₂
       │     ├── Waiting Time
       │     └── Throughput
       │
       └── Controls
             ├── Start
             ├── Stop
             └── Reset
```

---

# 🧪 Development Checkpoints

## End of Week 1

Each member demonstrates their isolated component:

```text
✅ SUMO Grid
✅ Gym Environment Skeleton
✅ FastAPI Server
✅ React Map
✅ Agreed JSON Schema
```

---

## End of Week 2

First real integration:

```text
SUMO
  ↓
FastAPI
  ↓
WebSocket
  ↓
React Map
```

And:

```text
SUMO + Gym
     ↓
Baseline PPO
     ↓
Visible Training Progress
```

---

## End of Week 3

Final integrated system:

```text
Trained PPO Agent
       ↓
Controls SUMO Traffic Lights
       ↓
FastAPI / WebSocket
       ↓
Real-Time React Dashboard
       ↓
Traffic + CO₂ Heatmap
       ↓
Live Performance Metrics
```

---

# 🌿 Why EcoFlux-RL?

Traditional traffic optimization:

```text
🚗 Move vehicles faster
        ↓
⏱️ Reduce waiting time
```

EcoFlux-RL:

```text
🚗 Traffic Efficiency
        +
🌫️ Environmental Impact
        ↓
🤖 Reinforcement Learning
        ↓
🚦 Intelligent Signal Control
        ↓
🌱 Sustainable Urban Mobility
```

The project demonstrates the application of Reinforcement Learning to an urban sustainability problem by combining traffic efficiency with environmental considerations.

---

# 🔮 Future Scope

The project can be extended in several directions:

- 🌍 Real-world traffic datasets
- 🏙️ Larger city networks
- 🤖 Multi-Agent Reinforcement Learning
- 🌦️ Weather-aware emission modeling
- 🌫️ Additional pollutant modeling
- ☁️ Cloud deployment
- ⚡ Edge deployment
- 🚦 Real-world traffic signal integration
- 📈 Advanced carbon forecasting
- 🏙️ City-scale traffic simulation

---

# 🔀 Git & Branching Strategy

The project follows a feature-branch workflow.

```text
main
 │
 ├── feature/simulation
 │
 ├── feature/rl-agent
 │
 ├── feature/backend-api
 │
 └── feature/frontend
```

### Development Flow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Add changes
git add .

# Commit
git commit -m "feat: add your feature"

# Push
git push origin feature/your-feature
```

Then create a Pull Request and merge after review.

### Commit Examples

```text
feat: add SUMO city grid
feat: implement PPO environment
feat: add FastAPI simulation endpoint
feat: implement WebSocket streaming
feat: add CO2 heatmap
fix: resolve simulation state mismatch
docs: update project architecture
```

---

# 🐳 Docker

Docker will be used during the final integration phase to make the system reproducible across different development environments.

Planned services:

```text
┌─────────────────────┐
│     Frontend        │
│       React         │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│      Backend        │
│ FastAPI + WebSocket │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ Simulation + RL     │
│ SUMO + PPO          │
└─────────────────────┘
```

---

# 📚 Documentation

Detailed documentation will be maintained inside:

```text
docs/
│
├── architecture.md
├── api.md
└── rl_design.md
```

Documentation will be updated as the project progresses.

---

# 🚧 Current Development Progress

### Overall Status

**🟢 Active Development**

| Module | Status |
|---|---|
| GitHub Repository | 🟢 Initialized |
| Project Architecture | 🟢 Planned |
| SUMO Simulation | 🟡 In Development |
| RL Environment | 🟡 In Development |
| PPO Agent | ⚪ Planned |
| FastAPI Backend | 🟡 In Development |
| WebSocket Streaming | ⚪ Planned |
| React Dashboard | 🟡 In Development |
| CO₂ Heatmap | ⚪ Planned |
| Final Integration | ⚪ Planned |
| Docker Deployment | ⚪ Planned |

### Legend

```text
🟢 Completed / Ready
🟡 In Development
⚪ Planned
🔴 Blocked
```

> Progress indicators will be updated throughout the 3-week development cycle.

---

# 🏁 Final Deliverable

The final system aims to provide:

```text
┌─────────────────────────────────────────────────────┐
│                  ECOFLUX-RL                         │
│                                                     │
│  🚗 Urban Traffic Simulation                        │
│            +                                        │
│  🤖 Multi-Objective PPO Agent                       │
│            +                                        │
│  🌫️ Carbon / Emission Monitoring                   │
│            +                                        │
│  ⚡ FastAPI + WebSocket                             │
│            +                                        │
│  🗺️ Real-Time React Dashboard                       │
│            ↓                                        │
│  🌱 Carbon-Aware Intelligent Traffic Control        │
└─────────────────────────────────────────────────────┘
```

---

# 🤝 Contributing

Contributions and suggestions are welcome.

### Steps

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test your changes
5. Commit your changes
6. Push your branch
7. Create a Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 🌱 EcoFlux-RL

<p align="center">
  <b>Smarter Traffic • Cleaner Air • Better Cities</b>
</p>

<p align="center">
  Built with 🤖 Reinforcement Learning, 🚦 Traffic Simulation and 🌱 Sustainability in mind.
</p>

<p align="center">
  ⭐ Star this repository if you find the project interesting!
</p>
