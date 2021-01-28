drop function get_all_players_data();
create or replace function get_all_players_data()
returns table (
        player_id int,
        index_name varchar,
        kickoff_time timestamp,
        selected int,
        minutes int,
        goals_conceded int,
        goals_scored int,
        threat decimal,
        creativity decimal,
        influence decimal,
        assists int,
        total_points int
)
language plpgsql
as $$

begin
    RETURN QUERY
    select players.player_id, players.index_name, player_gameweek_stats.kickoff_time, player_gameweek_stats.selected,
        player_gameweek_stats.minutes, player_gameweek_stats.goals_conceded, player_gameweek_stats.goals_scored,
        player_gameweek_stats.threat, player_gameweek_stats.creativity, player_gameweek_stats.influence,
        player_gameweek_stats.assists, player_gameweek_stats.total_points
    from players
    inner join player_gameweek_stats on players.player_id=player_gameweek_stats.player_id;
end;$$
