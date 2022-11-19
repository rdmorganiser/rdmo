export function updateConfig(config) {
  return {type: 'config/updateConfig', config}
}
export function updateConfigAndLocation(config) {
  return {type: 'config/updateConfigAndLocation', config}
}
