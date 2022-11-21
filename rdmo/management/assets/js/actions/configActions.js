import _ from 'lodash'

import * as elementActions from './elementActions'

export function updateConfig(config) {
  return (dispatch, getState) => {
    // first update the config, then call fetchElements
    dispatch({type: 'config/updateConfig', config})

    if (config.resourceType) {
      if (config.resourceId) {
        dispatch(elementActions.fetchElement(config))
      } else {
        dispatch(elementActions.fetchElements(config))
      }
    }
  }
}
export function updateLocation(config) {
  return {type: 'config/updateLocation', config}
}
export function updateConfigAndLocation(config) {
  return (dispatch, getState) => {
    // first update the config, then call updateLocation with the new state
    dispatch(updateConfig(config))
    dispatch(updateLocation(getState().config))
  }
}
