import { actions as errorActions } from '../reducers/errorsSlice'
import { actions } from '../reducers/templateSlice'
import { serializeError } from '../utils/errors'

import CoreApi from '../api/CoreApi'

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
  return errorActions.setError({
    source: 'templates',
    error: { ...serializeError(errors), context: gettext('Templates') }
  })
}
