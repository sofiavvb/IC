# Optimal Decision Trees via Integer Linear Programming

Undergraduate directed research project at the University of Campinas (Unicamp), advised by Prof. Dr. Rafael Crivellari Saliba Schouery.

This repository contains the implementation and experimental results of a flow-based Integer Linear Programming (ILP) formulation for generating optimal decision trees, based on the work of Aghaei et al. (2024).

## Background

Traditional decision tree algorithms such as CART build trees greedily, making locally optimal splits at each node. While efficient, this approach does not guarantee a globally optimal tree. Optimal decision tree methods instead formulate tree construction as an optimization problem, seeking the tree that maximizes classification accuracy globally.

This project studies ILP techniques for optimal decision tree generation, analyzing the trade-offs between accuracy, interpretability, sparsity, and computational scalability. The problem is NP-Hard, which makes the study of efficient formulations and solver behavior especially relevant.

## Formulation

The implementation follows the flow-based ILP formulation proposed by Aghaei et al. (2024). Given a fixed tree depth `d`, the model:

- Represents each internal node's branching decision via binary variables `b_(n,f)`
- Models data flow through the tree via binary variables `z_(i,n)`
- Assigns a single class to each leaf via binary variables `w_(l,c)`
- **Maximizes** the number of correctly classified training instances

All constraints enforce flow conservation, correct routing based on feature values, and valid leaf-class assignments. The model is solved using the [Gurobi](https://www.gurobi.com) ILP solver.

## Experiments

Experiments were conducted on 12 benchmark datasets from the UCI repository with only categorical features, across tree depths `d ∈ {2, 3, 4, 5}`. Each instance ran with a 1-hour time limit and a single thread.

| Instance        |  I   |  F  | K |
|----------------|------|-----|---|
| soybean-small  |  47  | 45  | 4 |
| monk3          | 122  | 15  | 2 |
| monk1          | 124  | 15  | 2 |
| hayes-roth     | 132  | 15  | 3 |
| monk2          | 169  | 15  | 2 |
| house-votes-84 | 232  | 16  | 2 |
| spect          | 267  | 22  | 2 |
| breast-cancer  | 277  | 38  | 2 |
| balance-scale  | 625  | 20  | 3 |
| tic-tac-toe    | 958  | 27  | 2 |
| car-evaluation | 1728 | 20  | 4 |
| kr-vs-kp       | 3196 | 38  | 2 |

*I = number of instances, F = number of features, K = number of classes*

Key findings:
- Instances with depth `d ≥ 4` frequently exceeded the time limit, consistent with the exponential growth of model size with depth
- Smaller instances (e.g. `soybean-small`) solved quickly across all depths
- Counterintuitively, some instances solved faster at greater depths — likely because a deeper tree fits the data more cleanly, improving branch-and-bound pruning

Full execution times and solver metrics are available in `experiments/`.

## Dependencies

- Python 3.10+
- [Gurobi 12.0.0](https://www.gurobi.com) (requires a valid license — free academic licenses available)
- `gurobipy`, `pandas`

## Usage

Run a single experiment:
```bash
python run_experiment.py --depth 3 --input datasets/categorical/monk1.csv
```

Run all experiments in parallel:
```bash
python run_all_experiments.py
```

Parse Gurobi logs into CSV:
```bash
./parser.py experiments/depth_3/monk1/
```

## References

- Aghaei, S., Gómez, A., & Vayanos, P. (2024). *Strong Optimal Classification Trees*. Operations Research. https://doi.org/10.1287/opre.2021.0034
- Bertsimas, D., & Dunn, J. (2017). *Optimal classification trees*. Machine Learning, 106(7). https://doi.org/10.1007/s10994-017-5633-9
- Hyafil, L., & Rivest, R. L. (1976). *Constructing optimal binary decision trees is NP-complete*. Information Processing Letters, 5(1).