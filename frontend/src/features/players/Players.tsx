import type { JSX } from "react"
import { useState } from "react"
import clsx from "clsx"
import {
  useGetPlayersQuery,
  type Player,
} from "./playersApiSlice"

const POS = [
  'batters',
  'pitchers',
  'c',
  '1b',
  '2b',
  '3b',
  'ss',
  'of',
  'ut',
  'sp',
  'rp'
]

export const Players = (): JSX.Element | null => {
  const {
    data: players,
    isLoading,
    isError,
    isFetching,
    isSuccess
  } = useGetPlayersQuery();
  const [searchString, setSearchString] = useState('')
  const [posFilter, setPosFilter] = useState('')
  const [allPlayers, setAllPlayers] = useState(false)

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

  const handlePositionClick = (pos: string) => {
    console.log(pos)
    if (pos === posFilter) {
      setPosFilter('')
    }
    setPosFilter(pos)
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
      className="flex flex-col w-full h-screen bg-amber-300 p-5"
    >
      <div
        className="h-full flex flex-col"
      >
        <div
          className="h-content"
        >
          <div>
            <input
              className="w"
              onChange={handleInputChange}
              value={searchString}
            ></input>
          </div>
          <div className="flex flex-row">
            <div className="flex flex-row">
              {POS.map(p => (
                <FilterButton
                  key={p}
                  className={clsx(p === posFilter && 'bg-amber-200')}
                  clickFunction={() => { handlePositionClick(p) }}
                >
                  {p}
                </FilterButton>
              ))}
              <FilterButton
                className={clsx(allPlayers && 'bg-amber-200')}
                clickFunction={
                  () => { setAllPlayers(true) }
                }
              >
                All Players
              </FilterButton>
              <FilterButton
                className={clsx(!allPlayers && 'bg-amber-200')}
                clickFunction={
                  () => { setAllPlayers(false) }
                }
              >
                Free Agents
              </FilterButton>
            </div>
            <div>
            </div>
          </div>
        </div>
        <div
          // result
          className="flex flex-col grow overflow-y-scroll"
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
      </div>
    </div >
  )
}

type FilterButtonProps = {
  children: React.ReactNode
  clickFunction: Function
  className?: string
}

const FilterButton = ({ children, className, clickFunction, ...props }: FilterButtonProps): JSX.Element => {
  const baseStyle = "rounded-2xl border-blue-800 border-2 min-w-10 bg-amber-50 px-3 mx-0.5"
  const allClasses = clsx(
    baseStyle,
    className,
  )

  return (
    <button className={allClasses} onClick={clickFunction} {...props}>
      {children}
    </button>
  )
}