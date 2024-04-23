import { isNil } from 'lodash'

import PageApi from '../api/PageApi'
import ProjectApi from '../api/ProjectApi'
import ValueApi from '../api/ValueApi'

import { updateLocation } from '../utils/location'
import { getAttributes, initPage } from '../utils/page'
import { initSets } from '../utils/set'
import { initValues } from '../utils/value'
import projectId from '../utils/projectId'

import ValueFactory from '../factories/ValueFactory'
import SetFactory from '../factories/SetFactory'

import {
  FETCH_NAVIGATION_ERROR,
  FETCH_NAVIGATION_SUCCESS,
  FETCH_OVERVIEW_ERROR,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_PAGE_ERROR,
  FETCH_PAGE_SUCCESS,
  FETCH_PROGRESS_ERROR,
  FETCH_PROGRESS_SUCCESS,
  FETCH_VALUES_SUCCESS,
  FETCH_VALUES_ERROR,
  STORE_VALUE_SUCCESS,
  STORE_VALUE_ERROR,
  DELETE_VALUE_SUCCESS,
  DELETE_VALUE_ERROR,
  CREATE_SET,
  DELETE_SET_SUCCESS,
  DELETE_SET_ERROR
} from './actionTypes'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

export function fetchOverview() {
  return (dispatch) => ProjectApi.fetchOverview(projectId)
    .then((overview) => dispatch(fetchOverviewSuccess(overview)))
    .catch((errors) => dispatch(fetchOverviewError(errors)))
}

export function fetchOverviewSuccess(overview) {
  return {type: FETCH_OVERVIEW_SUCCESS, overview}
}

export function fetchOverviewError(errors) {
  return {type: FETCH_OVERVIEW_ERROR, errors}
}

export function fetchProgress() {
  return (dispatch) => ProjectApi.fetchProgress(projectId)
    .then((progress) => dispatch(fetchProgressSuccess(progress)))
    .catch((errors) => dispatch(fetchProgressError(errors)))
}

export function fetchProgressSuccess(progress) {
  return {type: FETCH_PROGRESS_SUCCESS, progress}
}

export function fetchProgressError(errors) {
  return {type: FETCH_PROGRESS_ERROR, errors}
}

export function fetchNavigation(sectionId) {
  return (dispatch) => ProjectApi.fetchNavigation(projectId, sectionId)
    .then((navigation) => dispatch(fetchNavigationSuccess(navigation)))
    .catch((errors) => dispatch(fetchNavigationError(errors)))
}

export function fetchNavigationSuccess(navigation) {
  return {type: FETCH_NAVIGATION_SUCCESS, navigation}
}

export function fetchNavigationError(errors) {
  return {type: FETCH_NAVIGATION_ERROR, errors}
}

export function fetchPage(pageId) {
  return (dispatch) => {
    const promise = isNil(pageId) ? PageApi.fetchContinue(projectId)
                                  : PageApi.fetchPage(projectId, pageId)
    return promise.then((page) => {
      updateLocation(page.id)
      dispatch(fetchNavigation(page.section.id))
      dispatch(fetchPageSuccess(page))
      dispatch(fetchValues())
    })
  }
}

export function fetchPageSuccess(page) {
  return {type: FETCH_PAGE_SUCCESS, page: initPage(page)}
}

export function fetchPageError(errors) {
  return {type: FETCH_PAGE_ERROR, errors}
}

export function fetchValues() {
  return (dispatch, getStore) => {
    const page = getStore().interview.page

    return ValueApi.fetchValues(projectId, { attribute: getAttributes(page) })
      .then((values) => dispatch(fetchValuesSuccess(values, page)))
      .catch((errors) => dispatch(fetchValuesError(errors)))
  }
}

export function fetchValuesSuccess(values, page) {
  const sets = initSets(values)
  return {type: FETCH_VALUES_SUCCESS, values: initValues(values, sets, page), sets}
}

export function fetchValuesError(errors) {
  return {type: FETCH_VALUES_ERROR, errors}
}

export function storeValue(value) {
  return (dispatch) => {
    if (isNil(value.file)) {
      // obnly store the value
      return ValueApi.storeValue(projectId, value)
        .then((value) => dispatch(storeValueSuccess(value)))
        .catch((errors) => dispatch(storeValueError(errors)))
    } else {
      // first store the file
      return ValueApi.storeFile(projectId, value)
        .then((value) => {
          // then store the value
          return ValueApi.storeValue(projectId, value)
            .then((value) => dispatch(storeValueSuccess(value)))
            .catch((errors) => dispatch(storeValueError(errors)))
        })
        .catch((errors) => dispatch(storeValueError(errors)))
    }
  }
}

export function storeValueSuccess(value) {
  return {type: STORE_VALUE_SUCCESS, value}
}

export function storeValueError(errors) {
  return {type: STORE_VALUE_ERROR, errors}
}

export function createValue(attrs) {
  return storeValue(ValueFactory.create(attrs))
}

export function updateValue(value, attrs) {
  return storeValue(ValueFactory.update(value, attrs))
}

export function deleteValue(value) {
  return (dispatch) => {
    return ValueApi.deleteValue(projectId, value)
      .then(() => dispatch(deleteValueSuccess(value)))
      .catch((errors) => dispatch(deleteValueError(errors)))
  }
}

export function deleteValueSuccess(value) {
  return {type: DELETE_VALUE_SUCCESS, value}
}

export function deleteValueError(errors) {
  return {type: DELETE_VALUE_ERROR, errors}
}

export function activateSet(set) {
  return updateConfig('rdmo.interview', 'page.currentSetIndex', set.set_index)
}

export function createSet(attrs) {
  return (dispatch) => {
    // create a new set
    const set = SetFactory.create(attrs)

    // create a value for the text if the page has an attribute
    const value = isNil(attrs.attribute) ? null : ValueFactory.create(attrs)

    if (isNil(value)) {
      dispatch(activateSet(set))
      return dispatch({type: CREATE_SET, set})
    } else {
      return dispatch(storeValue(value)).then(() => {
        dispatch(activateSet(set))
        return dispatch({type: CREATE_SET, set})
      })
    }
  }
}

export function updateSet(setValue, attrs) {
  return storeValue(ValueFactory.update(setValue, attrs))
}

export function deleteSet(set, setValue) {
  if (isNil(setValue)) {
    // TODO: delete all values for all questions in the set
  } else {
    return (dispatch, getState) => {
      return ValueApi.deleteSet(projectId, setValue)
        .then(() => {
          const sets = getState().interview.sets.filter((s) => (s.set_prefix == set.set_prefix))

          if (sets.length > 1) {
            const index = sets.indexOf(set)
            if (index > 0) {
              dispatch(activateSet(sets[index - 1]))
            } else if (index == 0) {
              dispatch(activateSet(sets[1]))
            }
          }

          dispatch(deleteSetSuccess(set))
        })
        .catch((errors) => dispatch(deleteSetError(errors)))
    }
  }
}

export function deleteSetSuccess(set) {
  return {type: DELETE_SET_SUCCESS, set}
}

export function deleteSetError(errors) {
  return {type: DELETE_SET_ERROR, errors}
}
