Features

Implemented
* Game playable
* Input arbitrary number of players
* Input arbitrary task space size

To be done:
* Worker has to work down difficulty of task (simple iterator)
* Vary difficulty of each task
* Able to assign different ability to each worker. Impacts how many work units (difficulty points) they are able to handle each time step
* Ability to plan path. Whether they follow the path or not (opportunistic or rigid follower)
* Collect all intended moves and then resolve (have different conflict attributes)
* return key outcomes of each game. E.g. number of steps to completion (or got stuck)
* Be able to set whether or not tasks must be completed in a certain order
* Be able to set whether actors can only do tasks adjacent to the one they are currently on (in other words, the ability to get stuck)
