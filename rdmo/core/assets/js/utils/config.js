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
  deleteConfigInLocalStorage,
  getConfigFromLocalStorage,
  isTruthy,
  setConfigInLocalStorage
}
