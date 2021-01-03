select players.player_id, player_gameweek_stats.total_points, players.last_name
from players
inner join player_gameweek_stats on players.player_id=player_gameweek_stats.player_id;