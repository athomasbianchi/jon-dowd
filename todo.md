DATA_DONE
* Created Player Universe with tjid
* Cleaned Existing Contracts with tjid
* 2026 Draft Picks
* Team Database
* Create ESPN elig DB
* Create Player Info
* Projections
* Contracts

CURRENT
Isolate outputs
Archive init process

Cleanup folder structure [Reference](https://gist.github.com/ericmjl/27e50331f24db3e8f957d1fe7bbbe510)
create_id_map.py 
create_info.py 
create_pick_matrix.py 
fun_w_contracts.py 
get_espn_players.py 
get_teams.py 
handle_projections.py 
process_contracts.py 
process_espn_eligibility.py

NEXT
Cleanup process (all column names snake_case)
Create lineup DB (Check w/ Bob) ()
Handle new fangraphs prospects when it drops
Get fg data programatically?
<!-- https://www.fangraphs.com/api/projections?type=atc&stats=bat&pos=all&team=0&players=0&lg=all&z=1770917651291&download=1 -->
Update missing mlb_ids
Update org / age / etc for intl and prospects
build a runner?

LATER DATA
Future Draft Picks
Clean up MLBAMIDs by align name fixes with fangraphs name
Cleanup process to export w/ updated imports
  update: (projections, positions, teams,)
  grow: (id_map )
Get projections automatically?

FRONTEND
Roster View
Contracts View
Team View
* Add Logins?

IN-SEASON
Updates TeamIds, Positions, etc. as season goes (real-life trades, etc)


FUTURE OFFSEASON
Progress contracts to next season
Update Player Universe w new players