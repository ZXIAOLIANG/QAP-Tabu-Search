# Tabu Search for Quadratic Assignment Problem
Tabu Search are implemented and investigated to solve QAP in ECE457A. The distance and flow matrices are defined in `Distance.csv` and `Flow.csv`. The Tabu Search algorithm is defined in class `Tabu_search`.

## Output
`Tabu.py` outputs the initial solution used and the final solution found and its cost, it also outputs the specific configuration of the search, which can be specified in the code. It also indicates whether the best solution is found and the number of iterations. 

Sample output:
```bash
best solution reached
number of iterations: 55
initial solution: [17, 8, 0, 14, 16, 5, 12, 11, 15, 1, 13, 2, 10, 3, 7, 18, 19, 4, 9, 6]
tabu_list_length: 10
dynamic_tabu: False
aspiration: False
less_neighbourhood: False
frequency_based: False
solution: [16, 8, 1, 9, 18, 15, 17, 11, 0, 2, 6, 7, 10, 3, 13, 5, 19, 4, 14, 12]
cost: 2570.0
```

