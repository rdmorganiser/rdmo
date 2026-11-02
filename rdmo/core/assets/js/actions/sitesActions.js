import { actions } from '../reducers/sitesSlice'

import CoreApi from '../api/CoreApi'

import * as errorActions from './errorsActions'

export function fetchSites() {
  return function (dispatch) {
    dispatch(errorActions.clearError('sites'))

    return CoreApi.fetchSites()
      .then(sites => {
        dispatch(actions.fetchSitesSuccess(sites))
      })
      .catch(error => {
        dispatch(errorActions.setError('sites', error, gettext('Sites')))
        throw error
      })
  }
}
