import { actions as errorActions } from '../reducers/errorsSlice'
import { actions } from '../reducers/sitesSlice'
import { serializeError } from '../utils/errors'

import CoreApi from '../api/CoreApi'

export function fetchSites() {
  return function (dispatch) {
    dispatch(errorActions.clearError('sites'))

    return CoreApi.fetchSites()
      .then(sites => {
        dispatch(actions.fetchSitesSuccess(sites))
      })
      .catch(error => {
        dispatch(errorActions.setError({
          source: 'sites',
          error: { ...serializeError(error), context: gettext('Sites') }
        }))
        throw error
      })
  }
}
