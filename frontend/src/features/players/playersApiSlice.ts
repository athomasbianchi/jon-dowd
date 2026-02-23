import { createApi, fakeBaseQuery } from "@reduxjs/toolkit/query/react"
import supabase from '../../utils/supabase'

export type Player = {
  tj_id: string
  name: string
  name_ascii: string
  position: string
  team: string
  contract_dollars: number
  contract_years: number
  player_mlb_org: string
  player_pos: string
}

type PlayersApiResponse = {
  data: Player[]
}

export const playersApiSlice = createApi({
  baseQuery: fakeBaseQuery(),
  endpoints: (builder) => ({
    getPlayers: builder.query<PlayersApiResponse, void>({
      queryFn: async () => {
        // let returnData: Player[] = []
        // let fetching = true
        // let range_low = 0
        // let range_high = range_low + 999

        // while (fetching) {
          const { data, error } = await supabase
            .from('players')
            .select("*")
            .order('contract_dollars', { ascending: false, nullsFirst: false })
            .order('contract_years', { ascending: false, nullsFirst: false })
            // .range(range_low, range_high)
          if (error) {
            throw new Error(error.message || "Unknown error occurred while fetching players");
          }
          return { data }
          // returnData = [...returnData, ...(data as Player[])]
          // if ((data as Player[]).length < 1000) fetching = false
          // // fetching = false
          // range_low += 1000
          // range_high += 1000
        // }

        // return { data: returnData }
      },
    })
  })
})

export const { useGetPlayersQuery } = playersApiSlice
