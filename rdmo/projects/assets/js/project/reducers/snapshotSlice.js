import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  snapshots: null
}

const snapshotSlice = createSlice({
  name: 'snapshot',
  initialState,
  reducers: {
    fetchProjectSnapshotsSuccess(state, action) {
      state.snapshots = action.payload
    },
    createSnapshotSuccess(state, action) {
      state.snapshots = [action.payload, ...(state.snapshots || [])]
    },
    updateSnapshotSuccess(state, action) {
      state.snapshots = state.snapshots?.map(s => (
        s.id === action.payload.id ? { ...s, ...action.payload } : s
      ))
    },
    deleteSnapshotSuccess(state, action) {
      state.snapshots = state.snapshots?.filter(s => s.id !== action.payload)
    },
    rollbackSnapshotSuccess(state, action) {
      state.snapshots = action.payload
    }
  }
})

export const actions = snapshotSlice.actions

export default snapshotSlice.reducer
