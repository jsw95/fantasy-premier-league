from ortools.linear_solver import pywraplp
import uuid


def main(budget=200):
    """
    This handles the picking of the most point scoring team, within constraints.
    Constraints:
        - Cost < budget (100m)
        - 2 GKP, 5 DEF, 5 MID, 3 FWD
    """

    test_data = {
        "Alice": {"cost": 10, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 2},
        "Bob": {"cost": 20, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 0},
        "Charlie": {"cost": 21, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 1},
        "Dave": {"cost": 10, "n_gkp": 1, "n_def": 0, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 10},
        "def1": {"cost": 10, "n_gkp": 0, "n_def": 1, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 10},
        "def2": {"cost": 10, "n_gkp": 0, "n_def": 1, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 12},
        "def3": {"cost": 10, "n_gkp": 0, "n_def": 1, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 12},
        "def4": {"cost": 10, "n_gkp": 0, "n_def": 1, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 12},
        "def5": {"cost": 10, "n_gkp": 0, "n_def": 1, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()), "points": 12},
        "def6": {"cost": 10, "n_gkp": 0, "n_def": 1, "n_mid": 0, "n_fwd": 0, "id": str(uuid.uuid4()),"points": 12},
    }

    constraint_dict = {
        "cost": {"min": 0, "max": budget},
        "n_gkp": {"min": 2, "max": 2},
        "n_def": {"min": 5, "max": 5},
        # "n_mid": {"min": 5, "max": 5},
        # "n_fwd": {"min": 3, "max": 3},
    }


    # adding a unique id constraint to ensure players selected only once
    player_ids = [player['id'] for player in test_data.values()]
    for player_data in test_data.values():
        id_dict = {player_id: 0 for player_id in player_ids}
        id_dict[player_data['id']] = 1
        player_data.update(id_dict)
    for player_id in player_ids:
        constraint_dict[player_id] = {"min": 0, "max": 1}

    solver = pywraplp.Solver.CreateSolver('GLOP')
    objective = solver.Objective()

    players = {}

    for name, player_data in test_data.items():
        players[name] = solver.NumVar(0, solver.infinity(), name)
        objective.SetCoefficient(players[name], player_data['points'])

    objective.SetMaximization()

    # constraints = [0] * len(constraint_dict.items())
    # setting constraints
    for i, (constraint_name, constraint_info) in enumerate(constraint_dict.items()):
        constraint = solver.Constraint(constraint_info['min'], constraint_info['max'])
        for name, player_data in test_data.items():
            constraint.SetCoefficient(players[name], player_data[constraint_name])


    status = solver.Solve()
    if status == solver.OPTIMAL:
        price = 0
        for name, player_data in test_data.items():
            price += players[name].solution_value()
            print(name)
            print(players[name].solution_value())
            print()
if __name__ == "__main__":
    main()