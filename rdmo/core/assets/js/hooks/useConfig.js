import { useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { updateConfig } from '../actions/configActions'
import { selectConfig } from '../reducers/configSlice'

const useConfig = (path, defaultValue) => {
  const dispatch = useDispatch()

  const value = useSelector((state) => selectConfig(state, path, defaultValue))
  const setValue = useCallback((value) => dispatch(updateConfig(path, value)), [dispatch, path])

  return [value, setValue]
}

export default useConfig
