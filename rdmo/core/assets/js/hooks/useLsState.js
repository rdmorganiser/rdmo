import { useState } from 'react'
import { isEmpty, isPlainObject, omit as lodashOmit } from 'lodash'

import { checkStoreId } from '../utils/store'

const useLsState = (path, initialValue, omit = []) => {
  checkStoreId()

  const getLs = (path) => {
    const data = JSON.parse(localStorage.getItem(path))
    return isPlainObject(data) ? lodashOmit(data, omit) : data
  }

  const setLs = (path, value) => {
    const data = isPlainObject(value) ? lodashOmit(value, omit) : value
    localStorage.setItem(path, JSON.stringify(data))
  }

  const getInitialState = () => {
    // get the value from the local storage
    const lsValue = getLs(path)

    // return the state with the value from the local storage or the provided initialValue
    if (isPlainObject(lsValue)) {
      return { ...initialValue, ...lsValue }
    } else if (isEmpty(lsValue)) {
      return initialValue
    } else {
      return lsValue
    }
  }

  // setup the state
  const [value, setValue] = useState(getInitialState())

  return [
    value,
    (value) => {
      setLs(path, value)
      setValue(value)
    },
    () => setValue(getInitialState())
  ]
}

export default useLsState
