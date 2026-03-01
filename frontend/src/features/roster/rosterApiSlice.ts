import { createApi, fakeBaseQuery } from "@reduxjs/toolkit/query/react"
import supabase from '../../utils/supabase'
import type { Player } from '../players/playersApiSlice'

type RosterApiResponse = {
  data: Player[]
}

export const rosterApiSlice = createApi({
  reducerPath: 'rosterApi',
  baseQuery: fakeBaseQuery(),
  endpoints: (builder) => ({
    getTeamRoster: builder.query<RosterApiResponse, number>({
      queryFn: async (team_id) => {
        const { data, error } = await supabase
          .from('players')
          .select("*")
          .eq('team_id', team_id)
        if (error) {
          throw new Error(error.message || "Unknown error occurred while fetching team roster");
        }
        return { data }
      }
    })
  })
})

export const { useGetTeamRosterQuery } = rosterApiSlice
