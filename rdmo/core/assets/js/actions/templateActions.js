import { actions } from '../reducers/templateSlice'

import CoreApi from '../api/CoreApi'

import * as errorActions from './errorsActions'

export function fetchTemplates() {
  return function(dispatch) {
    dispatch(fetchTemplatesInit())

    return CoreApi.fetchTemplates()
      .then((templates) => dispatch(fetchTemplatesSuccess(templates)))
      .catch((errors) => dispatch(fetchTemplatesError(errors)))
  }
}

export function fetchTemplatesInit() {
  return errorActions.clearError('templates')
}

export function fetchTemplatesSuccess(templates) {
  return actions.fetchTemplatesSuccess(templates)
}

export function fetchTemplatesError(errors) {
  return errorActions.setError('templates', errors, gettext('Templates'))
}
