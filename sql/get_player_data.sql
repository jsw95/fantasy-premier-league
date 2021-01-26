drop function get_player_data(player_name varchar);
create or replace function get_player_data(player_name varchar)
returns table (
        player_id int,
        kickoff_time timestamp,
        total_points INT,
        last_name varchar
)
language plpgsql
as $$

begin
    RETURN QUERY
    select players.player_id, player_gameweek_stats.kickoff_time, player_gameweek_stats.total_points, players.last_name
    from players
    inner join player_gameweek_stats on players.player_id=player_gameweek_stats.player_id
    where players.index_name=player_name;
end;$$

