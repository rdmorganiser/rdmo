import { parseLocation } from '../utils/locations'
import * as configActions from '../actions/configActions'

export default function addEventListener(dispatch, getState) {
  window.addEventListener('popstate', (event) => {
    const config = parseLocation('/management/', event.target.location.pathname)
    dispatch(configActions.updateConfig(config))
  });
}
