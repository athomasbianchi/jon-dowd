import "./App.css"
import supabase from './utils/supabase';
import { useState, useEffect } from "react";

export const App = () => {
  const [players, setPlayers] = useState([])
  const [yb, setYB] = useState([])
  const [teams, setTeams] = useState([])


  const getPlayers = async () => {
    const { data: players, error } = await supabase
      .from('players')
      .select()
    console.log(players)
    setPlayers(players)
    // setPlayers(player_universe)
  }

  const getYB = async () => {
    const { data: yb, error } = await supabase
      .from('yb')
      .select()
      setYB(yb)
  }

  const getTeams = async () => {
    const { data: teams, error } = await supabase
      .from('teams')
      .select()
      .eq('team_level', 'majors')
    console.log(teams)
  }

  useEffect(() => {
    getPlayers()
    getYB()
    getTeams()
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
