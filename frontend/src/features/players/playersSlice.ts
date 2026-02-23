// import type { PayloadAction } from "@reduxjs/toolkit"
import { createAppSlice } from "../../app/createAppSlice"
// import type { AppThunk } from "../../app/store"

type Player = {
  name: string;
}

export type PlayersSliceState = {
  playerList: Player[]
}

const initialState: PlayersSliceState = {
  playerList: []
}

export const playersSlice = createAppSlice({
  name: "players",
  initialState,
  reducers: create => ({
    
  }),
  selectors: {}
})