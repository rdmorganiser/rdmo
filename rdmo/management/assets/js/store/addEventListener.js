import { parseLocation } from '../utils/locations'
import * as configActions from '../actions/configActions'

export default function addEventListener(dispatch, getState) {
  const getConfigFromLocation = (event) => {
    const config = parseLocation(getState().config.baseUrl, event.target.location.pathname)
    dispatch(configActions.updateConfig(config))
  }

  window.addEventListener('load', getConfigFromLocation)
  window.addEventListener('popstate', getConfigFromLocation)
}
