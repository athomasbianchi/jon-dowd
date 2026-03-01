import type { JSX } from "react"
import { useGetAaaContractsQuery, useUpdateAAAContractMutation } from "./aaaApiSlice"

const TEAMS: Record<string, string> = {
  '1': 'CR',
  '2': 'SF',
  '3': 'BS',
  '4': 'RW',
  '5': 'DET',
  '6': 'ORl',
  '7': 'SZ',
  '8': 'DCT',
  '9': 'YB',
  '10': 'CS',
  '19': 'MJ',
  '20': 'WCS',
}

export const AAATracker = (): JSX.Element | null => {
  const {
    data,
    isLoading,
    isError,
    isFetching,
    isSuccess
  } = useGetAaaContractsQuery();

  if (!isSuccess) {
    return (
      <div>
        Loading...
      </div>
    )
  }

  return (
    <div>
      {data.map((player) => (
        <AAAPlayer player={player} key={player.tj_id} />
      ))}
    </div>
  )
}

const AAAPlayer = ({ player }) => {
  // const player = useGetAaaContractsQuery()
  return (
    <div key={player.tj_id} className="flex flex-row">
      <div className="w-1/6">{player.players.name}</div>
      <div className="w-1/20">{TEAMS[player.team_id]}</div>
      <div className="w-1/20">{player.players.player_pos}</div>
      <div className="w-1/20">{player.players.player_mlb_org}</div>
      <div className="w-1/20">{player.picked_up}</div>
      <div className="w-1/20">{player.players.total_25}</div>
      <PickupSelect tj_id={player.tj_id} picked_up={player.picked_up} />
    </div>)
}

const PickupSelect = ({ tj_id, picked_up }: { tj_id: string, picked_up: boolean | null }) => {
  const [updateAaaContract, result] = useUpdateAAAContractMutation();

  let value = picked_up === null ? 'tbd' : picked_up ? 'picked_up' : 'declined';


  const handleChange = async (e) => {
    const pickup_obj = {
      'picked_up': true,
      'declined': false,
      'tbd': null
    }

    try {
      await updateAaaContract({
        tj_id,
        picked_up: pickup_obj[e.target.value]
      }).unwrap().then((payload) => console.log(payload))
    } catch (err) {
      console.error(err)
    }
  }


  return (
    <>
      <select onChange={handleChange} value={value}>
        <option value='tbd'>TBD</option>
        <option value='picked_up'>Pick Up</option>
        <option value='declined'>Decline</option>
      </select>
    </>
  )
} 