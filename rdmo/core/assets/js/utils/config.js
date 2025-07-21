import { set, unset } from 'lodash'

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
  updateConfig,
  deleteConfig,
  getConfigFromLocalStorage,
  setConfigInLocalStorage,
  deleteConfigInLocalStorage,
  isTruthy
}
