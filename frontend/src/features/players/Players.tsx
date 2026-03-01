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
  const [posFilter, setPosFilter] = useState('batters')
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
    if (pos === posFilter) {
      setPosFilter('')
    }
    setPosFilter(pos)
  }

  const nameFilter = (player: Player) => {
    return player.name_ascii
      .toLowerCase().trim()
      .includes(searchString.toLowerCase().trim())
  }

  const positionFilter = (player: Player) => {
    if (!posFilter) return true;
    const posObj: Record<string, string[]> = {
      'batters': ['c', '1b', '2b', '3b', 'ss', 'of', 'util'],
      'pitchers': ['sp', 'rp'],
      'c': ['c'],
      '1b': ['1b'],
      '2b': ['2b'],
      '3b': ['3b'],
      'ss': ['ss'],
      'of': ['of'],
      'ut': ['util'],
      'sp': ['sp'],
      'rp': ['rp']
    }

    const positionsArray: string[] = posObj[posFilter];
    return positionsArray.some(pos => player[pos as keyof Player])
  }

  const faFilter = (player: Player) => {
    if (allPlayers) return true
    return !player.team_id
  }

  const filteredPlayers: Player[] = Array.isArray(players)
    ? players.filter(nameFilter).filter(positionFilter).filter(faFilter) as Player[]
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
          className="flex-col flex grow overflow-y-scroll"
        >
          {filteredPlayers.map(player => {
            return (
              <FaPlayer player={player} key={player.tj_id} />
            )
          })}
        </div>
      </div>
    </div >
  )
}

type FilterButtonProps = {
  children: React.ReactNode
  clickFunction: React.MouseEventHandler<HTMLButtonElement>
  className?: string
}

const FilterButton = ({ children, className, clickFunction, ...props }: FilterButtonProps): JSX.Element => {
  const baseStyle = "rounded-2xl border-blue-800 border-2 min-w-10 bg-amber-50 px-3 mx-0.5"
  const allClasses = clsx(
    baseStyle,
    className,
  )

  return (
    <button
      className={allClasses}
      onClick={clickFunction} {...props}>
      {children}
    </button>
  )
}

type FaPlayerProps = {
  player: Player
}

export const TEAMS: Record<string, string> = {
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

const FaPlayer = ({ player }: FaPlayerProps): JSX.Element => {

  return (
    <div
      className="flex flex-row"
      onClick={() => { console.log(player.tj_id) }}
    >
      <div
        className="w-1/3"
      >{player.name} {playerPosString(player)} {player.player_mlb_org}</div>
      <div className="w-1/6">{TEAMS[String(player.team_id)] || 'FA'}</div>
      <div className="w-1/6">{player.fp_e}</div>
    </div>
  )
}

export const playerPosString = (player: Player): string => {
  const hittingPos = ['c', '3b', '2b', 'ss', '1b', 'of']
  let str = '';
  hittingPos.forEach(pos => {
    if (player[pos as keyof Player]) {
      if (str.length === 0) str = str.concat(pos.toUpperCase())
      else str = str.concat(`\\${pos.toUpperCase()}`)
    }
  })
  if (str.length === 0 && player.util) str = str.concat('UTIL')
  const pitchingPos = ['sp', 'rp']
  pitchingPos.forEach(pos => {
    if (player[pos as keyof Player]) {
      if (str.length === 0) str = str.concat(pos.toUpperCase())
      else str = str.concat(`\\${pos.toUpperCase()}`)
    }
  })
  return str
}