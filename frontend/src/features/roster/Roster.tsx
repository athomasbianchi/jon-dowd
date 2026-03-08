import { type JSX, useReducer } from "react"
import { useGetTeamRosterQuery, useUpdateRosterSlotMutation } from "./rosterApiSlice"
import { TEAMS, playerPosString } from '../players/Players'

const CAP = 100

// # SLOTS
// # 0 C
// # 1 1B
// # 2 2B
// # 3 3B
// # 4 SS
// # 5 OF
// # 6 MI
// # 7 CI
// # 8 LF
// # 9 CF
// # 10 RF
// # 11 DH
// # 12 UTIL
// # 13 P
// # 14 SP
// # 15 RP
// # 16 BE
// # 17 IL
// # 19 IF

// roster def
// c 1 (0)
// 1b 1 (1)
// 2b 1 (2)
// 3b 1 (3)
// ss 1 (4)
// of 3 (5)
// util (12)
// sp 5 (14)
// rp 2 (15)
// be 7 (16)
// aaa 12 (20)
// aa 15 (21)
// IL (17)
// 60-Day IL (60)

const ROSTER_SPOTS = {
  c: 0,
  '1b': 1,
  '2b': 2,
  '3b': 3,
  ss: 4,
  of: 5,
  util: 12,
  sp: 14,
  rp: 15,
  be: 16,
  aaa: 20,
  aa: 21,
  il: 17,
  '60': 60
}


export const Team = ({ team_id }: { team_id: number }): JSX.Element | null => {
  const {
    data,
    isLoading,
    isError,
    isFetching,
    isSuccess,
    status
  } = useGetTeamRosterQuery(team_id)
  if (!isSuccess) return <div>Loading...</div>

  const sal = data.map(x => x.contract_dollars).reduce((a, b) => a + b)

  const sorted = [...data].sort((a, b) => (b.contract_dollars - a.contract_dollars))

  return (
    <div>
      {sorted.map(x => {
        return (
          <Player player={x} />
        )
      })}
    </div>
  )
}

const PosSelector = ({ player }) => {
  const [updateRosterSlot, result] = useUpdateRosterSlotMutation();
  const pos = {
    c: player.c,
    '1b': player['1b'],
    '2b': player['2b'],
    '3b': player['3b'],
    ss: player.ss,
    of: player.of,
    util: player.util,
    sp: player.sp,
    rp: player.rp
  }
  const posArray = Object.keys(pos).filter(x => pos[x])

  const handleRosterSlot = async (e) => {
    const result = await updateRosterSlot({
      contract_id: player.contract_id,
      roster_spot: ROSTER_SPOTS[e.target.value]
    }).unwrap().then((payload) => console.log(payload))
  }

  return (
    <select onChange={(e) => handleRosterSlot(e)}>
      <option value="">choose a position</option>
      {posArray.map(pos => (
        <option value={pos}>{pos.toUpperCase()}</option>
      ))}
      <option value="be">Bench</option>
      <option value="aaa">AAA</option>
      <option value="aa">AA</option>
    </select>
  )
}

const Player = ({ player }) => {
  return (
    <div
      key={player.tj_id}
    >
      {player.name}
      {' '}{playerPosString(player)}
      {' '}{player.contract_dollars}
      {' '}{player.roster_spot}
      {' '}<PosSelector
        player={player}
      />
    </div>
  )
}

