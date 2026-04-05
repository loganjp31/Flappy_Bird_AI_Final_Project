# Flappy Bird AI Using a Genetic Algorithm

## Overview

This project implements an AI-controlled version of Flappy Bird using a Genetic Algorithm. Instead of manual input, a population of agents learns to play the game by evolving decision-making parameters over multiple generations. The objective is to maximize survival time and the number of pipes successfully passed.

---

## Features

- Fully functional Flappy Bird game environment
- AI-controlled agents
- Genetic Algorithm for learning and optimization
- Fitness-based evolution across generations
- Real-time simulation and scoring

---

## AI Approach

Each agent makes decisions based on the current state of the game. The input features used for decision-making are:

- Bird height
- Bird vertical velocity
- Horizontal distance to the next pipe
- Pipe gap position
- Bias term

At each frame, a decision score is computed using weighted inputs. If the score exceeds a threshold, the bird performs a jump action.

### Actions
- Jump
- Do nothing

### Fitness Function

The performance of each agent is evaluated using the following fitness criteria:

- +5 for passing a pipe
- -2 for colliding with the ground
- -2 for colliding with a pipe
- +0.1 for every second survived

### Genetic Algorithm Process

1. Initialize a population of agents with random weights  
2. Evaluate each agent based on its fitness  
3. Select parent agents using fitness-proportional selection  
4. Perform crossover to combine parent weights  
5. Apply mutation with a small probability  
6. Generate a new population  
7. Repeat over multiple generations  

---

## System Design

The system is composed of the following core components:

- **Game Engine**: Handles rendering, physics, collision detection, and scoring  
- **Agent (Bird)**: Represents an individual with decision-making weights and fitness  
- **Environment (Pipes and Ground)**: Generates obstacles and updates positions  
- **Genetic Algorithm Module**: Manages selection, crossover, mutation, and evolution  

### Data Flow

1. The game updates the environment and agent states  
2. Each agent observes the current game state  
3. The agent computes a decision and acts  
4. The environment updates based on the action  
5. Fitness is updated continuously  
6. Once all agents fail, a new generation is created  

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

## Controls

The system is fully AI-controlled. No manual input is required during execution.

## Course Context

This project was developed for SOFE3720: Introduction to Artificial Intelligence. It demonstrates the application of AI techniques to a dynamic environment, including problem formulation, algorithm implementation, system design, and performance evaluation.

## Ethical Considerations

This system highlights the importance of objective function design in AI systems. The behavior of the agents is directly influenced by the defined fitness function. Careful consideration must be given to how performance metrics are constructed, as they determine the learning outcomes of the system.

## Authors

Logan Jones Patterson
Sharujan Sivanandam

## License

This project is intended for academic use.
