import type { JSX } from "react"
import { useState } from "react"
// import styles from "./Quotes.module.css"
import {
  useGetPlayersQuery,
  type Player,
} from "./playersApiSlice"

export const Players = (): JSX.Element | null => {
  const {
    data: players,
    isLoading,
    isError,
    isFetching,
    isSuccess
  } = useGetPlayersQuery();
  const [searchString, setSearchString] = useState('')

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchString(e.target.value)
  }

  if (!isSuccess) {
    return (
    <div>
      <div>Loading {isLoading}</div>
      <div>Error {isError}</div>
      <div>isFetching {isFetching}</div>
    </div>
    )
  }

  const filteredPlayers: Player[] = Array.isArray(players)
    ? players.filter((player: Player) =>
        player.name_ascii
          .toLowerCase()
          .includes(searchString.toLowerCase())
      ) as Player[]
    : [];


  return (
    <div
      className="flex flex-col w-full h-screen bg-amber-300"
    >
      <div
      >
        <input
          onChange={handleInputChange}
          value={searchString}
        ></input>
        {searchString}
      </div>
      <div
        // result
        className="flex flex-col"
      >
        {filteredPlayers.map(player => {
          return (
            <div
              key={player.tj_id}
              className="flex flex-row">
                {player.name}{" "}
                {player.player_mlb_org}{" "}
                {player.player_pos}
            </div>
          )
        })}
      </div>
      hi
    </div >
  )
}