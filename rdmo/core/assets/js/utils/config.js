import { set, unset, toNumber, isNaN } from 'lodash'

const updateConfig = (config, path, value) => {
  const newConfig = {...config}
  set(newConfig, path, value)
  return newConfig
}

const deleteConfig = (config, path) => {
  const newConfig = {...config}
  unset(newConfig, path)
  return newConfig
}

const getConfigFromLocalStorage = (prefix) => {
  const ls = {...localStorage}

  return Object.entries(ls)
    .filter(([lsPath,]) => lsPath.startsWith(prefix))
    .map(([lsPath, lsValue]) => {
      if (lsPath.startsWith(prefix)) {
        const path = lsPath.replace(`${prefix}.`, '')

        // check if it is literal 'true' or 'false'
        if (lsValue === 'true') {
          return [path, true]
        } else if (lsValue === 'false') {
          return [path, false]
        }

        // check if the value is number or a string
        const numberValue = toNumber(lsValue)
        if (isNaN(numberValue)) {
          return [path, lsValue]
        } else {
          return [path, numberValue]
        }
      } else {
        return null
      }
    })
}

const setConfigInLocalStorage = (prefix, path, value) => {
  localStorage.setItem(`${prefix}.${path}`, value)
}

const deleteConfigInLocalStorage = (prefix, path) => {
  localStorage.removeItem(`${prefix}.${path}`)
}

export {
  updateConfig,
  deleteConfig,
  getConfigFromLocalStorage,
  setConfigInLocalStorage,
  deleteConfigInLocalStorage
}
