import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  issues: null
}

const keepState = state => state

const issueSlice = createSlice({
  name: 'issue',
  initialState,
  reducers: {
    fetchProjectIssuesSuccess(state, action) {
      state.issues = action.payload
    },
    updateProjectIssueSuccess: keepState,
    sendProjectIssueEmailSuccess: keepState,
    sendProjectIssueIntegrationSuccess: keepState
  }
})

export const actions = issueSlice.actions

export default issueSlice.reducer
