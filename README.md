# 🌱 EcoFlux-RL
## Reinforcement Learning for Urban Carbon-Aware Traffic Signal Optimization

EcoFlux-RL is a Reinforcement Learning-based system designed to optimize urban traffic signal control while reducing **vehicle waiting time, traffic congestion, fuel consumption, and carbon emissions**.

This branch focuses on the **Reinforcement Learning / Machine Learning module** of the EcoFlux-RL project.

---

## 👨‍💻 Member 2 — RL / ML Module

The RL/ML module is responsible for developing and evaluating intelligent traffic signal control agents using **Reinforcement Learning**.

The agent observes the current traffic conditions and learns which traffic signal action should be taken to improve traffic flow while minimizing congestion and carbon emissions.

---

## 🎯 Objectives

The main objectives of this module are:

- Design a custom Reinforcement Learning environment
- Define traffic-related observation and action spaces
- Develop a carbon-aware reward function
- Train RL agents using PPO
- Compare RL performance against traditional traffic signal baselines
- Evaluate trained agents using traffic and environmental metrics
- Export trained models for inference and integration

---

## 🧠 Reinforcement Learning Approach

The system follows the standard Reinforcement Learning loop:

```text
Traffic Environment
       ↓
   Observation
       ↓
   RL Agent
       ↓
      Action
       ↓
Traffic Signal Control
       ↓
   Environment
       ↓
     Reward
       ↓
   RL Agent
