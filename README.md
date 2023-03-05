# optimal-path-using-dijkstras-algorithm
 This python project is the result of a class assignment for [Colorado State 
 University course WR 514:  GIS and Data Analysis in Water Resources](https://www.online.colostate.edu/courses/WR/WR514.dot).  

 The python script uses [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
 to optimize the past of least "cost" based on an [adjacency matrix](https://people.revoledu.com/kardi/tutorial/GraphTheory/Adjacency-Matrix.html#:~:text=Adjacency%20Matrix%20of%20a%20Graph&text=To%20fill%20the%20adjacency%20matrix,this%20number%20as%20matrix%20element.&text=The%20matrix%20to%20represent%20a,way%20is%20called%20Adjacency%20matrix%20.) 
 provided by the user.

 Code was adapted from a helpful tutorial found on [geeksforgeeks.org](https://www.geeksforgeeks.org/printing-paths-dijkstras-shortest-path-algorithm/).

 ## Problem 1:

Town A requires a new source of water from River E. The terrain between the town and the river is such that a variety of alternative routes are available, each involving 4 pumping stations and different levels of expenditure. It has been decided that there are four possible locations for the pump intake of water from the river (at points E1-E4) and 12 possible intermediate locations for the three pumping stations (B1 – B4, C1 – C4, and D1 – D4) through which the pipeline must pass as shown on the figure. The numbers attached to each link represent the construction cost and the number in each box is the cost of the pumping station at that location.

The problem is to find the pipeline route linking river E with town A resulting in minimum cost. Treat the problem as multi-stage process using the dynamic programming (DP) concept.

image1

## Problem 2:
Write the LP matrix to solve for the shortest path for the network below (i.e. travel from node 1 to node 12). The numbers adjacent to the arrows are the costs (or travel times) associated with the arcs. Solve the model using. an LP solver of your choice.

image2
