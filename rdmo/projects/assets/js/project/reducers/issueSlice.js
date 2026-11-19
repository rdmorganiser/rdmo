import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  issues: null
}

const keepState = state => state

const issueSlice = createSlice({
  name: 'issue',
  initialState,
  reducers: {
    fetchProjectIssuesInit: keepState,
    fetchProjectIssuesSuccess(state, action) {
      state.issues = action.payload
    },
    fetchProjectIssuesError: keepState,
    updateProjectIssueInit: keepState,
    updateProjectIssueSuccess: keepState,
    updateProjectIssueError: keepState,
    sendProjectIssueEmailInit: keepState,
    sendProjectIssueEmailSuccess: keepState,
    sendProjectIssueEmailError: keepState,
    sendProjectIssueIntegrationInit: keepState,
    sendProjectIssueIntegrationSuccess: keepState,
    sendProjectIssueIntegrationError: keepState
  }
})

export const actions = issueSlice.actions

export default issueSlice.reducer
