# Vaccum World Problem 
in this repository we try to solve the problem of cleaning a grid of blocks with a vacuum cleaner. we try various environments with different conditions and test different agents on them to overcome the challenges that comes with these conditions.

This repository consists of two main parts, **environment** and **agents**.

## Environment
Our environment implementation meets many conditions, each of which can present a different challenge. These conditions include:

- **Probability of having dirt in a block**: This property specifies how likely a block can become dirty

- **Probability of having obstacle in the map**: This property determines our environment has obstacles or not and also with what probability any block in the environment can be an obstacle that the agent cannot pass.

- **Uncertainty of the presence of dirt in the block**:  This property specifies that the clean room can become dirty after each step with a fixed probability.

- **Uncertainty of performing an action**: For this one, you can specify whether you want this property for the "Suck" action or move, or both. If you enable this feature with fixed probability, some agent functions will not be performed.

- **Uncertainty about the accuracy of an observation**: This property gives your environment the ability to give false information about the presence of dirt in a block with a fixed probability.

- **Disable the location sensor**: This feature allows your environment to not provide any information about the location of the agent in the environment

You can create environments with arbitrary dimensions and using these built in conditions you can create different challenges for the agents you made yourself. Note that by default, the initial state of each agent in this environment is (0,0). It can be said that every vacuum cleaner has a fixed location.

## Agents
in this repository, we create and implement various agents with various functionality. We explain each one below:
- **Reflexive agent (for two room)**: This agent only works in two rooms that are next to each other. If the observation is [room left, clean/dirty], it goes to the right and vice versa. If it sees dirt in a room, it cleans it. We use this agent only in the first question (you can see the results in the notebook)

- **Random Reflexive agent**: this agent is very simple one, it chooses the movement action in a random way and if it sees a room that is dirty, cleans it. 

- **Agent with faulty dirt sensor**: This one uses the internal memory, which is an array with the dimensions of the environment, each element of which represents the probability of a block being dirty, the agent moves around the environment and updates the probabilities. If it clears the room, the prior probability is multiplied by 0.25, and if it just visits the block and passes it, the prior probability is multiplied by 0.1. The agent always chooses the block to go to that is more likely to be dirty. 

- **TraGent (tracing agent)**: This creates a path from the initial state to the end of the environment. If it is in goal-based mode, it will terminate the process there because it can be sure that it has visited all the blocks and cleared them all. But if it is in utility-based mode, it follows the path it has come so far. Because it looks for more dirty blocks to clean. 

- **Agent with no Location sensor**: This one uses the internal memory, which is an array of dimensions of the environment, each element of which represents an unvisited block of the environment (with a value of -1). the agent uses a BFS algorithm to find the nearest unobserved block around it. The agent uses a BFS algorithm to find the nearest unobserved block around it. When it finds the block, it tries to go to the block. if it encounters an obstacle, changes the value of that coordinate in the memory to 1, otherwise 0. Note that this agent has only two pieces of information about its location, its initial state, which is fixed inside the environment, and whether or not it has hit an obstacle. 

- **BFS Agent**: This agent follows a model-based approach. It uses a fixed model of the environment to find the optimal path in the map with the BFS algorithm. Note that the agent does not change or update anything in the model and is only used to check the current state of the environment. The agent does not have access to information about whether the room is dirty or not. 




