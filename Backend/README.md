# EcoTwin Backend

Backend API for the EcoTwin urban traffic and carbon dispersal simulation project.

The backend manages traffic simulation using Eclipse SUMO and TraCI, maintains simulation state, integrates the Reinforcement Learning (RL) service, and provides real-time simulation updates through WebSocket.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Eclipse SUMO
- TraCI
- WebSocket
- Reinforcement Learning service

## Backend Features

- Simulation start, stop and reset
- Simulation status monitoring
- Simulation step execution
- SUMO integration using TraCI
- Real-time WebSocket simulation streaming
- Vehicle count tracking
- Simulation time tracking
- RL service integration
- RL action generation
- RL service initialization and reset
- RL action persistence in simulation state
- Swagger API documentation

## Project Structure

```text
Backend/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── routes/
│   │   ├── health.py
│   │   ├── simulation.py
│   │   └── rl.py
│   │
│   ├── schemas/
│   │   └── simulation.py
│   │
│   ├── services/
│   │   ├── simulation_service.py
│   │   └── rl_service.py
│   │
│   ├── simulation/
│   │   ├── state.py
│   │   └── sumo_client.py
│   │
│   └── websocket/
│       └── manager.py
│
├── sumo/
│   ├── network.net.xml
│   ├── routes.rou.xml
│   └── simulation.sumocfg
│
├── tests/
│   ├── test_sumo.py
│   └── test_websocket.py
│
├── requirements.txt
├── Dockerfile
└── README.md