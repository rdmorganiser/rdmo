import CoreApi from '../api/CoreApi'

import { FETCH_TEMPLATES_ERROR, FETCH_TEMPLATES_INIT, FETCH_TEMPLATES_SUCCESS } from './actionTypes'

export function fetchTemplates() {
  return function(dispatch) {
    dispatch(fetchTemplatesInit())

    return CoreApi.fetchTemplates()
      .then((templates) => dispatch(fetchTemplatesSuccess(templates)))
      .catch((errors) => dispatch(fetchTemplatesError(errors)))
  }
}

export function fetchTemplatesInit() {
  return {type: FETCH_TEMPLATES_INIT}
}

export function fetchTemplatesSuccess(templates) {
  return {type: FETCH_TEMPLATES_SUCCESS, templates}
}

export function fetchTemplatesError(errors) {
  return {type: FETCH_TEMPLATES_ERROR, errors}
}
