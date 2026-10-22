import { actions } from '../reducers/sitesSlice'
import { serializeError } from '../utils/errors'

import CoreApi from '../api/CoreApi'

export function fetchSites() {
  return function (dispatch) {
    dispatch(actions.fetchSitesInit())

    return CoreApi.fetchSites()
      .then(sites => {
        dispatch(actions.fetchSitesSuccess(sites))
      })
      .catch(error => {
        dispatch(actions.fetchSitesError(serializeError(error)))
        throw error
      })
  }
}
