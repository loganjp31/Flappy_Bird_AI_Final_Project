# Flappy Bird AI Using NEAT

## Overview

This project implements an AI-controlled version of Flappy Bird using **NEAT (NeuroEvolution of Augmenting Topologies)**. Instead of manually controlling the bird, a population of agents evolves over multiple generations to learn how to play the game.

Unlike a traditional Genetic Algorithm with a fixed neural network, NEAT allows both the **weights and the structure of the neural network** to evolve. This enables the system to discover increasingly complex strategies over time.

---

## Features

- Fully functional Flappy Bird game built with Pygame  
- AI-controlled agents using NEAT  
- Evolving neural network topology (not fixed)  
- Speciation to protect innovation  
- Elitism to preserve top-performing agents  
- Custom fitness function based on survival, performance, and positioning  
- Real-time simulation with generation tracking  
- Pause functionality for debugging and observation  

---

## AI Approach

Each agent is controlled by a neural network that evolves over time.

### Inputs

The neural network receives the following inputs:

- Bird height (`bird_y`)  
- Bird vertical velocity (`bird_vel`)  
- Horizontal distance to the next pipe (`pipe_dist`)  
- Vertical position of the pipe gap (`gap_y`)  
- Bias term  

### Output

- A single output node determines whether the bird should:
  - **Jump** (if output > threshold)
  - **Do nothing**

---

## NEAT Implementation

This project implements a simplified version of NEAT with the following components:

### Genome Representation

Each genome consists of:

- **Node genes**
  - Input, hidden, output, and bias nodes  
- **Connection genes**
  - Weighted connections between nodes  
  - Enabled/disabled state  
  - Innovation numbers for tracking  

### Key NEAT Features

- **Structural mutation**
  - Add connection
  - Add node (splitting existing connections)

- **Weight mutation**
  - Random perturbation or reassignment of weights  

- **Crossover**
  - Matching genes aligned by innovation numbers  
  - Excess/disjoint genes inherited from the fitter parent  

- **Speciation**
  - Genomes grouped by similarity  
  - Prevents new structures from being eliminated too early  

- **Elitism**
  - Top-performing genomes are preserved across generations  

---

## Fitness Function

The fitness of each agent is calculated at the end of each generation using:
```
fitness = frames_survived + (pipes_passed * 150) - (abs(bird.y - gap_center) * 0.1)
```



### Explanation

- **Frames survived** → rewards staying alive  
- **Pipes passed × 150** → strongly rewards progress  
- **Distance from gap penalty** → encourages stable positioning  

This creates a balanced objective that promotes both survival and intelligent movement.

---

## System Design

The system consists of the following components:

- **Game Engine**
  - Handles rendering, physics, and collisions  

- **Agent**
  - Wraps the bird and its neural network (genome)  

- **Genome**
  - Represents the neural network structure and weights  

- **Population**
  - Manages evolution, speciation, and reproduction  

- **Environment**
  - Pipes and ground mechanics  

### Data Flow

1. The environment updates (pipes, ground, positions)  
2. Each agent observes the current state  
3. The neural network computes an action  
4. The bird performs the action  
5. Statistics are tracked (frames survived, pipes passed)  
6. Fitness is calculated after all agents fail  
7. Population evolves into the next generation  

---

## Controls

- **P** → Pause / Unpause the simulation  

The system is otherwise fully AI-controlled.

---

## Requirements

- Python 3.10 or newer  
- pygame  
- pygbag (optional, for browser execution)  

---

## Installation

Create and activate a virtual environment:

## Installation

Create and activate a virtual environment:

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Local Execution

Run the main application:

```
python3 main.py
```

## Browser Execution with Pygbag

Run the following command in the project directory:
```
pygbag .
```

Open the generated local server URL in a browser to view the simulation.

## Course Context

This project was developed for SOFE3720: Introduction to Artificial Intelligence. It demonstrates the application of AI techniques to a dynamic environment, including problem formulation, algorithm implementation, system design, and performance evaluation.

## Ethical Considerations

This system highlights the importance of objective function design in AI systems. The behavior of the agents is directly influenced by the defined fitness function. Careful consideration must be given to how performance metrics are constructed, as they determine the learning outcomes of the system.

## Authors

Logan Jones Patterson
Sharujan Sivanandam

## License

This project is intended for academic use.

## References

- Original Flappy Bird game implementation (game and image foulders):
  https://github.com/siddharth-movaliya/Flappy-Bird-AI
