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
  return actions.fetchTemplatesInit()
}

export function fetchTemplatesSuccess(templates) {
  return actions.fetchTemplatesSuccess(templates)
}

export function fetchTemplatesError(errors) {
  return actions.fetchTemplatesError(serializeError(errors))
}
