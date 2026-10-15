import { Immer } from 'immer'
import { set, unset } from 'lodash'

// Keep freezing disabled locally for compatibility with the existing apps.
const { produce } = new Immer({ autoFreeze: false })

const updateConfig = (config, path, value) => produce(config, draft => {
  set(draft, path, value)
})

const deleteConfig = (config, path) => produce(config, draft => {
  unset(draft, path)
})

const getConfigFromLocalStorage = (prefix) => {
  const ls = {...localStorage}

  return Object.entries(ls)
    .filter(([lsPath,]) => lsPath.startsWith(prefix))
    .map(([lsPath, lsValue]) => (
      lsPath.startsWith(prefix) ? [lsPath.replace(`${prefix}.`, ''), lsValue] : null
    ))
}

const setConfigInLocalStorage = (prefix, path, value) => {
  localStorage.setItem(`${prefix}.${path}`, value)
}

const deleteConfigInLocalStorage = (prefix, path) => {
  localStorage.removeItem(`${prefix}.${path}`)
}

const isTruthy = (value) => [true, 'true'].includes(value)

export {
  deleteConfig,
  deleteConfigInLocalStorage,
  getConfigFromLocalStorage,
  isTruthy,
  setConfigInLocalStorage,
  updateConfig
}
