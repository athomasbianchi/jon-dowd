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
  contract_type: string
  aaa_options: boolean
  player_mlb_org: string
  player_pos: string
  team_id: number
  c: boolean
  '1b': boolean
  '2b': boolean
  '3b': boolean
  ss: boolean
  of: boolean
  util: boolean
  sp: boolean
  rp: boolean
  fp_e: number
  total_25: number
}

type PlayersApiResponse = {
  data: Player[]
}

export const playersApiSlice = createApi({
  reducerPath: 'playersApi',
  baseQuery: fakeBaseQuery(),
  endpoints: (builder) => ({
    getPlayers: builder.query<PlayersApiResponse, void>({
      queryFn: async () => {
        // TODO turn back on pagination

        // let returnData: Player[] = []
        // let fetching = true
        // let range_low = 0
        // let range_high = range_low + 999

        // while (fetching) {
          const { data, error } = await supabase
            .from('players')
            .select("*")
            .order('fp_e', { ascending: false, nullsFirst: false })
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
