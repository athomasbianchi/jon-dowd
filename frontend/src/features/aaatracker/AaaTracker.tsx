import type { JSX } from "react"
// import { useState } from "react"
// import clsx from "clsx"
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
        Hi
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
    <div key={player.tj_id}>
      {player.players.name}
      {TEAMS[player.team_id]}
      {player.players.player_pos}
      {player.players.player_mlb_org}
      {player.picked_up}
      <PickupSelect tj_id={player.tj_id} picked_up={player.picked_up} />
    </div>)
}

const PickupSelect = ({ tj_id, picked_up }: { tj_id: string, picked_up: boolean | null }) => {
  // const [value, setValue] = useS
  const [updateAaaContract, result ] = useUpdateAAAContractMutation();
  console.log(result)

  let value = picked_up === null ? 'tbd' : picked_up ? 'picked_up' : 'declined';


  const handleChange = async (e) => {
    console.log(tj_id)
    console.log(e.target.value)
    const pickup_obj = {
      'picked_up': true,
      'declined': false,
      'tbd': null
    }

    try {
      // const change = await updateAaaContract({
       await updateAaaContract({
        tj_id,
        picked_up: pickup_obj[e.target.value]
      }).unwrap().then((payload) => console.log(payload))
      // console.log(change) 
      // console.log(data)
    } catch (err) {
      console.error(err)
    }
  }
  // console.log(isLoading)


  return (
    <>
    <select onChange={handleChange} value={value}>
      <option value='tbd'>TBD</option>
      <option value='picked_up'>Pick Up</option>
      <option value='declined'>Decline</option>
    </select>
    <div>{result.status}</div>
    </>
  )
} 