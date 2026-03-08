import { createApi, fakeBaseQuery } from "@reduxjs/toolkit/query/react"
import supabase from '../../utils/supabase'
import type { Player } from '../players/playersApiSlice'

type RosterApiResponse = {
  data: Player[]
}

export const rosterApiSlice = createApi({
  reducerPath: 'rosterApi',
  baseQuery: fakeBaseQuery(),
  tagTypes: ['Roster'],
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
      },
      providesTags: ['Roster']
    }),
    updateRosterSlot: builder.mutation<void, { contract_id: string, roster_spot: number }>({
      queryFn: async ({ contract_id, roster_spot }) => {
        console.log(contract_id, roster_spot)
        const { data, error } = await supabase
          .from('contracts')
          .update({ roster_spot: roster_spot })
          .eq('contract_id', contract_id)
          .select()
        console.log(data, error)
        if (error) {
          throw new Error(error.message || "Unknown error occurred while updating roster slot");
        }
        return { data }
      },
      invalidatesTags: ['Roster']
    })
  })
})

export const {
  useGetTeamRosterQuery,
  useUpdateRosterSlotMutation
} = rosterApiSlice
