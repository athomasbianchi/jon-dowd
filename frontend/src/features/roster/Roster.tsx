import { type JSX, useReducer } from "react"
import { useGetTeamRosterQuery } from "./rosterApiSlice"
import { TEAMS, playerPosString } from '../players/Players'

const CAP = 100

// roster def
// c 1
// 1b 1
// 2b 1
// 3b 1
// ss 1
// of 3
// util 1
// sp 5
// rp 2
// be 7
// aaa 12
// aa 15

const rosterReducer = (state, action) => {
  console.log(action)
  switch (action.type) {
    case 'setSpot':
      return {
        ...state,
        [action.payload.pos]: [...state[action.payload.pos], action.payload.tj_id]
      }

    // case
    // if (action.type === ) {

    // }
  }
}

const initState = {
  c: [null],
  '1b': [null],
  '2b': [null],
  ss: [null],
  '3b': [null],
  util: [null],
  of: new Array(3).fill(null),
  sp: new Array(5).fill(null),
  rp: new Array(2).fill(null),
  be: [],
  aaa: [],
  aa: [],
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
  const [state, dispatch] = useReducer(rosterReducer, initState)
  if (!isSuccess) return <div>Loading...</div>
  console.log(state)


  const sal = data.map(x => x.contract_dollars).reduce((a, b) => a + b)

  const sorted = [...data].sort((a, b) => (b.contract_dollars - a.contract_dollars))

  return (
    <div>
      <div>{TEAMS[team_id]}</div>
      <div>{sal}</div>
      <div>{CAP - sal}</div>
      {state['c'].map(tj_id => {
        return (<div>C</div>)
      })}
      {state['1b'].map(tj_id => {
        return (<div>1B</div>)
      })}
      {state['2b'].map(tj_id => {
        return (<div>2B</div>)
      })}
      {state['3b'].map(tj_id => {
        return (<div>3B</div>)
      })}
      {state['ss'].map(tj_id => {
        return (<div>SS</div>)
      })}
      {state.of.map(tj_id => {
        return (<div>OF</div>)
      })}
      {state.util.map(tj_id => {
        return (<div>UTIL</div>)
      })}
      {sorted.map(x => {
        return (
          <div
            key={x.tj_id}
          >
            {x.name}
            {' '}{playerPosString(x)}
            {' '}{x.contract_dollars}
            {' '}<PosSelector
              player={x}
              dispatch={dispatch}
            />
          </div>
        )
      })}
    </div>
  )
}

const PosSelector = ({player, dispatch}) => {
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
  
  const handleSelect = (e) => {
    dispatch({type: 'setSpot', payload: {
      pos: e.target.value,
      tj_id: player.tj_id
    }})
  }

  return (
    <select onChange={(e) => handleSelect(e)}>
      {posArray.map(pos => (
        <option value={pos}>{pos.toUpperCase()}</option>
      ))}
      <option value="be">Bench</option>
      <option value="aaa">AAA</option>
      <option value="aa">AA</option>
    </select>
  )
}

