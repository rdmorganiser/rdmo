const getConfigFromLocalStorage = (prefix) => {
  const ls = {...localStorage}

  return Object.entries(ls)
    .filter(([lsPath,]) => lsPath.startsWith(`${prefix}.`))
    .map(([lsPath, lsValue]) => [lsPath.replace(`${prefix}.`, ''), JSON.parse(lsValue)])
}

const setConfigInLocalStorage = (prefix, path, value) => {
  localStorage.setItem(`${prefix}.${path}`, JSON.stringify(value))
}

const deleteConfigInLocalStorage = (prefix, path) => {
  localStorage.removeItem(`${prefix}.${path}`)
}

export {
  deleteConfigInLocalStorage,
  getConfigFromLocalStorage,
  setConfigInLocalStorage
}
