from ortools.linear_solver import pywraplp



def main(budget=20):
    """
    This handles the picking of the most point scoring team, within constraints.
    Constraints:
        - Cost < budget (100m)
        - 2 GKP, 5 DEF, 5 MID, 3 FWD
    """

    test_data = {
        "Alice": {"cost": 10, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "points": 2},
        "Bob": {"cost": 20, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "points": 0},
        "Charlie": {"cost": 21, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "points": 1},
        "Dave": {"cost": 10, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "points": 10},
    }

    constraint_dict = {
        "cost": {"min": 0, "max": budget},
        "n_gkp": {"min": 2, "max": 2},
        # "n_def": {"min": 5, "max": 5},
        # "n_mid": {"min": 5, "max": 5},
        # "n_fwd": {"min": 3, "max": 3},
    }

    solver = pywraplp.Solver.CreateSolver('GLOP')
    # points = solver.NumVar(0, solver.infinity(), 'cost')
    # cost = solver.NumVar(0, 1000, 'cost')
    # n_gkp = solver.NumVar(0, 1000, 'n_gkp')
    # n_def = solver.NumVar(0, 1000, 'n_def')
    # n_mid = solver.NumVar(0, 1000, 'n_mid')
    # n_fwd = solver.NumVar(0, 1000, 'n_fwd')
    #
    # solver.Add(cost <= budget)
    # solver.Add(n_gkp == 2)
    # solver.Add(n_def == 5)
    # solver.Add(n_mid == 5)
    # solver.Add(n_fwd == 3)

    objective = solver.Objective()

    players = [[]] * len(test_data)

    for i, (name, player_data) in enumerate(test_data.items()):
        players[i] = solver.NumVar(0, solver.infinity(), name)
        objective.SetCoefficient(players[i], 1)

    objective.SetMaximization()

    constraints = [0] * len(constraint_dict.items())
    # setting constraints
    for i, (constraint_name, constraint) in enumerate(constraint_dict.items()):
        constraints[i] = solver.Constraint(constraint['min'], constraint['max'])
        for j, (name, player_data) in enumerate(test_data.items()):
            constraints[i].SetCoefficient(players[j], player_data[constraint_name])


    status = solver.Solve()
    if status == solver.OPTIMAL:
        price = 0
        for i in range(len(test_data)):
            price += players[i].solution_value()
            print(players[i])
            print(players[i].solution_value())
            print()
if __name__ == "__main__":
    main()