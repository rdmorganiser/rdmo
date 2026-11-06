import { actions } from '../reducers/locationSlice'
import { updateLocation } from '../utils/location'

export function setLocation(location) {
  return (dispatch) => {
    // update the location in the url
    updateLocation(location)

    // update the location in the store
    dispatch(actions.setLocation(location))
  }
}
