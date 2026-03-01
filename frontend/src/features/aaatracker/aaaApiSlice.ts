import { createApi, fakeBaseQuery } from "@reduxjs/toolkit/query/react"
import supabase from '../../utils/supabase'

type AaaContract = {
  tj_id: string
  contract_id: string
  team_id: number
  picked_up: boolean
}

type AaaApiResponse = {
  data: AaaContract[]
}

export const aaaApiSlice = createApi({
  reducerPath: 'aaaApi',
  baseQuery: fakeBaseQuery(),
  tagTypes: ['AaaContracts'],
  endpoints: (builder) => ({
    getAaaContracts: builder.query<AaaApiResponse, void>({
      queryFn: async () => {
        const { data, error } = await supabase
          .from('aaa_26')
          .select("*, players!inner(tj_id, name, player_pos, player_mlb_org, fp_e)")
          .order('team_id', { ascending: true })
          // .order('total_25', { ascending: false, nullsFirst: false })
        if (error) {
          throw new Error(error.message || "Unknown error occurred while fetching AAA contracts");
        }
        return { data }
      },
      providesTags: ['AaaContracts']
    }),
    updateAAAContract: builder.mutation<AaaContract, { tj_id: string; picked_up: boolean | null }>({
      queryFn: async ({ tj_id, picked_up }) => {
        const { data, error } = await supabase
          .from('aaa_26')
          .update({ picked_up: picked_up })
          .eq('tj_id', tj_id)
          .select()
        // console.log(data, error)
        if (error) {
          throw new Error(error.message || "Unknown error occurred while updating AAA contract");
        }
        return { data }
      },
      invalidatesTags: ['AaaContracts']
    })
  })
})

export const {
  useGetAaaContractsQuery,
  useUpdateAAAContractMutation
} = aaaApiSlice