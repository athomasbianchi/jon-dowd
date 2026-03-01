import "./App.css"
import { Players } from "./features/players/Players";
import { AAATracker } from "./features/aaatracker/AaaTracker";
import { Team } from "./features/roster/Roster"

export const App = () => {
  return (
    <>
      {/* <Players />
      <AAATracker /> */}
      <Team team_id={9} />
    </>
  )
}
