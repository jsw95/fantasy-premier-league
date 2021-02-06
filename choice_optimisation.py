from ortools.linear_solver import pywraplp
import uuid
from pprint import pprint


def main(budget=200):
    """
    This handles the picking of the most point scoring team, within constraints.
    Constraints:
        - Cost < budget (100m)
        - 2 GKP, 5 DEF, 5 MID, 3 FWD
        - Max 3 from each team
        - Player can only be used once
    """

    test_data = {
        "Alice": {"cost": 10, "GKP": 1, "DEF": 0, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 2},
        "Bob": {"cost": 20, "GKP": 1, "DEF": 0, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 0},
        "Charlie": {"cost": 21, "GKP": 1, "DEF": 0, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 1},
        "Dave": {"cost": 10, "GKP": 1, "DEF": 0, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 10},
        "def1": {"cost": 10, "GKP": 0, "DEF": 1, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 10},
        "def2": {"cost": 10, "GKP": 0, "DEF": 1, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 12},
        "def3": {"cost": 10, "GKP": 0, "DEF": 1, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 12},
        "def4": {"cost": 10, "GKP": 0, "DEF": 1, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 12},
        "def5": {"cost": 10, "GKP": 0, "DEF": 1, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 12},
        "def6": {"cost": 10, "GKP": 0, "DEF": 1, "MID": 0, "FWD": 0, "id": str(uuid.uuid4()), "points": 12},
    }
    for i in range(200):
        test_data[f"fwd{i}"] = {"cost": i, "GKP": 0, "DEF": 0, "MID": 0, "FWD": 1, "id": str(uuid.uuid4()), "points": 12}
        test_data[f"mid{100-i}"] = {"cost": i, "GKP": 0, "DEF": 0, "MID": 1, "FWD": 0, "id": str(uuid.uuid4()), "points": 12}

    constraint_dict = {
        "cost": {"min": 0, "max": budget},
        "GKP": {"min": 2, "max": 2},
        "DEF": {"min": 5, "max": 5},
        "MID": {"min": 5, "max": 5},
        "FWD": {"min": 3, "max": 3},
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

    # setting constraints
    for i, (constraint_name, constraint_info) in enumerate(constraint_dict.items()):
        constraint = solver.Constraint(constraint_info['min'], constraint_info['max'])
        for name, player_data in test_data.items():
            constraint.SetCoefficient(players[name], player_data[constraint_name])

    status = solver.Solve()
    if status == solver.OPTIMAL:
        team_selection = {"GKP": [], "DEF": [], "MID": [], "FWD": []}
        for name, player_data in test_data.items():
            selected = round(players[name].solution_value())
            if selected:
                for position in team_selection.keys():
                    if player_data[position] == 1:
                        team_selection[position].append(name)
                        break

        print(team_selection)
        return team_selection
    else:
        print("No optimal solution found")

if __name__ == "__main__":
    main()
