# Deep Reinforcement Learning for Peg Solitaire
> IT3105 

The RL system is split into two parts; the environment and the agent. 
The environment contains all information about the game itself, like board, rules and states.
The agent contains an actor and a critic, and is the learning part of the system.

## The environment's tasks:
* Know the rules of the game
* Providing initial board state and successor states of any parent state
* Giving reward for moves
* Determining final state (is the game over?)

## The agent's tasks:
* Updating value tables for states, (hopefully) resulting in a successful policy
* Deciding actions
* Must have no references to problem domain
* Actor and critic __only__ communicates via the TD error

##### Specifically, the actor should:
* represent its policy as table/python dict that maps state-action pairs to values (values should be normalized for each state)
* be on-policy, i.e. target policy = behavior policy
* use epsilon-greedy strategy

##### And the critic should:
* contain two different implementations
    * Table implementation
    * Neural network implemented with either Tensorflow or PyTorch. 
    
    
Parameters of the system can be changed in [`config.yml`](config.yml)

At the end of each run, two things are displayed:
1. The progression of the learning, showing the number of remaining pegs for each episode
2. A complete run of the game showing all moves
