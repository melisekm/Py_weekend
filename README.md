# Py_weekend kiwi task

# Usage
```
python -m solution <CSV FILE> <ORIGIN_AIRPORT_CODE> <DESTINATION_AIRPORT_CODE> [--bags=<BAG_COUNT>] [--return]
```
Example:
```
python -m solution data.csv DHE NIZ --bags=2 --return
```
Results are printed to _stdout_

## Description

### Intro

Assignment: Write a python script/module/package, that for a given flight data in a form of csv file (check the examples),
prints out a structured list of all flight combinations for a selected route between airports A -> B, sorted by the final price for the trip.  
Search restrictions:
- In case of a combination of A -> B -> C, the layover time in B should not be less than 1 hour and more than 6 hours.
- No repeating airports in the same trip!

File structure:
```
├── src                <- Source code for use in this project.
│   ├── graph.py       <- Graph representation of problem. Performs the final search
│   │
│   ├── solution.py    <- Main script file. Used to run the project.
│   │
│   ├── solver.py      <- Initializes the search and prepares the output.
│   │
│   ├── utils.py       <- Utility functions
│   │
│   └── example        <- Test .csv files
│       └── example[0-3].csv
│
└── README.md
```

Script was implemented in Python v3.9.5 64bit. It is run by Command Line, PowerShell or other CLI tool. 
Program uses only the standard built-in library, no 3rd party tools are needed.

### Data representation
After reading the input data from csv file and parsing arguments we create multidigraph. As nodes we use airports and edges are flights between airports(nodes).
### Algorithm
Main algorithm to perform the search is Recursive Depth First Search (DFS) which is able to find all the combinations.  
We initialize the search beginning in the origin node and traverse the graph storing the visited vertices in a dictionary.
If we reach the destination node we make the temporal flight list permanent and unwind the recursion. We also move one level higher in the
recursion when we try all adjacent edges to the currently visited node. By keeping track of visited nodes we do not visit one node multiple times and when 
we unwind, we remove current path from temporal path list and mark the node again as unvisited.

After the search is done, we calculate remaining info about the paths and print out the json-compatible structured list of trips sorted by price.

### Optional arguments
```--bags=x``` - sets the number of requested bags. If one of the flights has max allowed 1 bag we can take only 1 bag with us on the whole trip. If this argument is set to _2_
we automatically ignore flights where we cant take both of our bags.  
```--return``` - Is it a return flight?	 - when we reach destination trip we perform new return trip beginning in the destination node and ending in the origin node.
Essentially we travel back to where we started.  
There is a note saying: **Since WIW is in this case the final destination for one part of the trip, the layover rule does not apply.** So we take this as a second part of a trip
so it is indeed possible to visit the airports already visited on first part of the trip once more.(again no more than once). Also the second rule about layover is not in place, so when we 
arrive at our destination at 10:00, we can leave 10:00 or 10:05 for a return trip. Same as if we wait 7 days and then make a return trip. Then again layover rule on the return trip starts to 
apply yet again, so no less than 1 hour or more than 6 hour layover.

### Complexity
Basically, we generate all possible paths from A and check whether they end up in B. The space is heavly pruned by the search layover rules and the **fact that if we have flights sorted by departure, 
we can immediately stop when the layover time exceeds 6 hours**. 
It is not infinite because we are looking only for simple paths  
Discussion on the complexity of this problem can be extensive, because if we think about it we have multidigraph where edges have their own identity.
We visit every vertex more than once and we have to try every possibility. Easly we can come up with scenario
where eventhough the simple path is clear, our algorithm has to explore every possible path which _may_ end up in goal node. Thus having complexity of **O(V!)**, 
but imagine this situation(not talking about flights, but graph in general):
We have three nodes. A B and C, we want to find all simple paths A - > C. There is only one path from B to C, but from A to B there is huge amount of paths. 
Everytime we unwind the recursion we have to check next and next edge and so on....

### Summary
This is a [classical problem](https://xlinux.nist.gov/dads/HTML/allSimplePaths.html) which was fun to think about and create a working solution. Which is hopefully correct.
Thanks.
