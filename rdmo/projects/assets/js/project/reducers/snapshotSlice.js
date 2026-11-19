import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  snapshots: null
}

const keepState = state => state

const snapshotSlice = createSlice({
  name: 'snapshot',
  initialState,
  reducers: {
    fetchProjectSnapshotsInit: keepState,
    fetchProjectSnapshotsSuccess(state, action) {
      state.snapshots = action.payload
    },
    fetchProjectSnapshotsError: keepState,
    createSnapshotInit: keepState,
    createSnapshotSuccess(state, action) {
      state.snapshots = [action.payload, ...(state.snapshots || [])]
    },
    createSnapshotError: keepState,
    updateSnapshotInit: keepState,
    updateSnapshotSuccess(state, action) {
      state.snapshots = state.snapshots?.map(s => (
        s.id === action.payload.id ? { ...s, ...action.payload } : s
      ))
    },
    updateSnapshotError: keepState,
    deleteSnapshotInit: keepState,
    deleteSnapshotSuccess(state, action) {
      state.snapshots = state.snapshots?.filter(s => s.id !== action.payload)
    },
    deleteSnapshotError: keepState,
    rollbackSnapshotInit: keepState,
    rollbackSnapshotSuccess(state, action) {
      state.snapshots = action.payload
    },
    rollbackSnapshotError: keepState
  }
})

export const actions = snapshotSlice.actions

export default snapshotSlice.reducer
