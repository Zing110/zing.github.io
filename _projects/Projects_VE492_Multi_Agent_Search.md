---
title: "Multi-Agent Search"
collection: projects
type: "Undergraduate project"
permalink: /projects/MASearch
venue: "SJTU-UM JI, ECE Department"
date: 2024-08-01
location: "Shanghai, China"
---

This Project aims to implement Multi-Agent Search Problem using python.

# Multi-Agent Search

**Multi-Agent Search** refers to the process of finding solutions to problems by coordinating multiple autonomous agents. These agents work together to explore the search space, make decisions, and achieve common or individual goals. Multi-agent search is a critical area of research in fields like artificial intelligence, robotics, and distributed systems, as it allows for solving complex problems more efficiently than single-agent approaches.

## Key Concepts

### **Agents**
- **Definition**: An agent is an entity that can perceive its environment and take actions based on its perceptions to achieve a goal.
- In the context of multi-agent search, multiple agents collaborate, either cooperatively or competitively, to solve a problem or explore a space.

### **Search Space**
- The search space is the domain or environment where agents search for solutions. This can be a grid, a graph, or a more abstract space like a set of possible states in a problem.

### **Cooperation vs. Competition**
- **Cooperative Multi-Agent Search**: All agents work together towards a common goal, sharing information and resources to find an optimal solution.
- **Competitive Multi-Agent Search**: Agents may have conflicting goals, such as in games or adversarial search, where each agent seeks to outperform or block the others.

### **Coordination**
- In multi-agent systems, coordination ensures that agents work together efficiently, avoiding redundant actions or conflicts.
  - **Task Allocation**: In a cooperative setup, agents must decide which tasks to undertake, often based on their individual capabilities or knowledge.
  - **Path Planning**: In environments with physical movement (e.g., robots), agents need to plan paths to avoid collisions and optimize travel time.


## Types of Multi-Agent Search Problems

1. **Cooperative Multi-Agent Search**
   - **Common Goal**: Multiple agents search for a single goal together, such as exploring an unknown area or finding the shortest path to a destination.
   - Example: Robots in a warehouse working together to pick up items or deliver packages.

2. **Competitive Multi-Agent Search**
   - **Adversarial Setting**: Agents are in competition, each striving to achieve their own goal at the expense of the others.
   - Example: Two or more players in a game trying to find the best strategy to win, such as in chess or Go.

3. **Exploration**
   - **Area Exploration**: Agents explore a given environment and discover new areas or objects.
   - Example: Search and rescue missions where multiple drones or robots explore an unknown disaster site.

4. **Pathfinding**
   - **Navigation**: Agents find paths through a shared environment while avoiding obstacles and other agents.
   - Example: Autonomous vehicles navigating through a city without collisions.

## Common Algorithms for Multi-Agent Search

1. **Centralized Approaches**
   - A central controller or planner manages the search for all agents. It can have global knowledge and compute optimal solutions for all agents.
   - **Advantages**: Can find globally optimal solutions.
   - **Disadvantages**: Single point of failure, scalability issues, and may require significant computation time.

2. **Decentralized Approaches**
   - Each agent operates independently, with no central authority. Agents share limited information with each other and work based on local knowledge.
   - **Advantages**: Scalable, fault-tolerant, and more flexible.
   - **Disadvantages**: Can lead to suboptimal solutions due to lack of global coordination.

3. **Multi-Agent A* Search**
   - An extension of the A* search algorithm where multiple agents search for paths in a shared environment. This approach often includes mechanisms to avoid collisions and ensure that agents do not interfere with each other’s paths.

4. **Priority-Based Planning**
   - Agents are assigned priorities, and high-priority agents are planned first, followed by lower-priority agents. This approach is often used in pathfinding problems to ensure that higher-priority agents do not get blocked by lower-priority ones.


## Applications of Multi-Agent Search

- **Robotics**: Coordinating robots in warehouses, autonomous vehicles, or search-and-rescue missions.
- **Gaming**: Multiplayer games or simulations where agents (players or AI entities) must search for strategies, resources, or optimal paths.
- **Distributed Problem Solving**: For example, collaborative filtering or recommendation systems where agents (users) search for relevant information.
- **Smart Grids**: Managing energy distribution in a network of distributed agents (smart meters, appliances, etc.).

## Conclusion

Multi-Agent Search is a powerful tool for solving complex problems that involve multiple entities working together or competing. By leveraging cooperation, communication, and efficient search strategies, multi-agent systems can tackle problems that are too difficult for single-agent systems. The balance between coordination, communication, and computation is key to optimizing performance and scalability in multi-agent search systems.


### Implementation:

The doc for how the requirement of the implementation is [Project explination](../assets/code/VE492/p3/p3.pdf).

The code files can be found [here](https://github.com/Zing110/VE492/tree/main/p3/p3)
