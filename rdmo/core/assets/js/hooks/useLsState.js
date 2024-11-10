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

  // get the value from the local storage
  const lsValue = getLs(path)

  // setup the state with the value from the local storage or the provided initialValue
  const [value, setValue] = useState(isEmpty(lsValue) ? initialValue : lsValue)

  return [
    value,
    (value) => {
      setLs(path, value)
      setValue(value)
    },
    () => {
      if (isPlainObject(initialValue)) {
        setValue({ ...initialValue, ...getLs(path) })
      } else {
        setValue(initialValue)
      }
    }
  ]
}

export default useLsState
