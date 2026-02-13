import "./App.css"
import supabase from './utils/supabase';
import { useState, useEffect } from "react";

export const App = () => {
  const [players, setPlayers] = useState([])


  const getPlayers = async () => {
    const { data: player_universe, error } = await supabase
      .from('player_universe')
      .select()
      .limit(10)
    console.log(player_universe)
    setPlayers(player_universe)
    // setPlayers(player_universe)
  }

  useEffect(() => {
    getPlayers()
  }, [])

  

  console.log(players)
  return (
    <div className="App">
      {players.map(player => (
        <div>{player.NameASCII}</div>
      ))}
    </div>
  )
}
