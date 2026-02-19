import "./App.css"
import supabase from './utils/supabase';
import { useState, useEffect } from "react";

export const App = () => {
  const [players, setPlayers] = useState([])
  const [yb, setYB] = useState([])


  const getPlayers = async () => {
    const { data: player_universe, error } = await supabase
      .from('player_universe')
      .select()
      .limit(10)
    console.log(player_universe)
    setPlayers(player_universe)
    // setPlayers(player_universe)
  }

  const getYB = async () => {
    const { data: yb, error } = await supabase
      .from('yb')
      .select()
      setYB(yb)
      console.log(yb)
  }

  useEffect(() => {
    getPlayers()
    getYB()
  }, [])

  

  return (
    <div className="App">
      {yb.sort((a,b) => (Number(a.player_age) - Number(b.player_age)) ).map(player => (
        <div key={player.tj_id}>
        <span
        >{player.name} </span>
        <span>{player.player_mlb_org} </span>
        <span>{player.player_age}</span>
        </div>
      ))}
    </div>
  )
}
