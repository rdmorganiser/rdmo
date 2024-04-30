import { isEmpty, isNil } from 'lodash'

import PageApi from '../api/PageApi'
import ProjectApi from '../api/ProjectApi'
import ValueApi from '../api/ValueApi'

import { updateLocation } from '../utils/location'

import { initPage } from '../utils/page'
import { gatherSets, getDescendants, initSets } from '../utils/set'
import { initValues } from '../utils/value'
import projectId from '../utils/projectId'

import ValueFactory from '../factories/ValueFactory'
import SetFactory from '../factories/SetFactory'

import {
  NOOP,
  FETCH_NAVIGATION_ERROR,
  FETCH_NAVIGATION_SUCCESS,
  FETCH_PAGE_ERROR,
  FETCH_PAGE_SUCCESS,
  FETCH_VALUES_SUCCESS,
  FETCH_VALUES_ERROR,
  CREATE_VALUE,
  STORE_VALUE_SUCCESS,
  STORE_VALUE_ERROR,
  DELETE_VALUE_SUCCESS,
  DELETE_VALUE_ERROR,
  CREATE_SET,
  DELETE_SET_SUCCESS,
  DELETE_SET_ERROR
} from './actionTypes'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

export function fetchPage(pageId) {
  if (pageId === 'done') {
    return (dispatch) => {
      updateLocation('done')
      dispatch(fetchNavigation(null))
      dispatch(fetchPageSuccess(null, true))
    }
  } else {
    return (dispatch) => {
      const promise = isNil(pageId) ? PageApi.fetchContinue(projectId)
                                    : PageApi.fetchPage(projectId, pageId)
      return promise.then((page) => {
        updateLocation(page.id)
        initPage(page)
        dispatch(fetchNavigation(page))
        dispatch(fetchValues(page))
        dispatch(fetchPageSuccess(page, false))
      })
    }
  }
}

export function fetchPageSuccess(page, done) {
  return {type: FETCH_PAGE_SUCCESS, page, done}
}

export function fetchPageError(errors) {
  return {type: FETCH_PAGE_ERROR, errors}
}

export function fetchNavigation(page) {
  return (dispatch) => {
    return ProjectApi.fetchNavigation(projectId, page && page.section.id)
      .then((navigation) => dispatch(fetchNavigationSuccess(navigation)))
      .catch((errors) => dispatch(fetchNavigationError(errors)))

  }
}

export function fetchNavigationSuccess(navigation) {
  return {type: FETCH_NAVIGATION_SUCCESS, navigation}
}

export function fetchNavigationError(errors) {
  return {type: FETCH_NAVIGATION_ERROR, errors}
}

export function fetchValues(page) {
  return (dispatch) => {
    return ValueApi.fetchValues(projectId, { attribute: page.attributes })
      .then((values) => dispatch(fetchValuesSuccess(values, page)))
      .catch((errors) => dispatch(fetchValuesError(errors)))
  }
}

export function fetchValuesSuccess(values, page) {
  const sets = gatherSets(values)

  initSets(sets, page)
  initValues(sets, values, page)

  return {type: FETCH_VALUES_SUCCESS, values, sets}
}

export function fetchValuesError(errors) {
  return {type: FETCH_VALUES_ERROR, errors}
}

export function storeValue(value) {
  return (dispatch, getStore) => {
    const valueIndex = getStore().interview.values.indexOf(value)
    const valueFile = value.file

    return ValueApi.storeValue(projectId, value)
      .then((value) => {
        if (isNil(valueFile)) {
          return dispatch(storeValueSuccess(value, valueIndex))
        } else {
          return ValueApi.storeFile(projectId, value, valueFile)
            .then((value) => dispatch(storeValueSuccess(value, valueIndex)))
            .catch((errors) => dispatch(storeValueError(errors)))
        }
      })
      .catch((errors) => dispatch(storeValueError(errors)))
  }
}

export function storeValueSuccess(value, valueIndex) {
  return {type: STORE_VALUE_SUCCESS, value, valueIndex}
}

export function storeValueError(errors) {
  return {type: STORE_VALUE_ERROR, errors}
}

export function createValue(attrs, store) {
  const value = ValueFactory.create(attrs)

  if (isNil(store)) {
    return {type: CREATE_VALUE, value}
  } else {
    return storeValue(value)
  }
}

export function updateValue(value, attrs) {
  return storeValue(ValueFactory.update(value, attrs))
}

export function deleteValue(value) {
  return (dispatch) => {
    if (isNil(value.id)) {
      return dispatch(deleteValueSuccess(value))
    } else {
      return ValueApi.deleteValue(projectId, value)
        .then(() => dispatch(deleteValueSuccess(value)))
        .catch((errors) => dispatch(deleteValueError(errors)))
    }
  }
}

export function deleteValueSuccess(value) {
  return {type: DELETE_VALUE_SUCCESS, value}
}

export function deleteValueError(errors) {
  return {type: DELETE_VALUE_ERROR, errors}
}

export function activateSet(set) {
  if (isEmpty(set.set_prefix)) {
    return updateConfig('rdmo.interview', 'page.currentSetIndex', set.set_index)
  } else {
    return { type: NOOP }
  }
}

export function createSet(attrs) {
  return (dispatch, getState) => {
    // create a new set
    const set = SetFactory.create(attrs)

    // create a value for the text if the page has an attribute
    const value = isNil(attrs.attribute) ? null : ValueFactory.create(attrs)

    // create an action to be called immediately or after saving the value
    const action = (value) => {
      dispatch(activateSet(set))

      const state = getState().interview

      const page = state.page
      const sets = [...state.sets, set]
      const values = isNil(value) ? [...state.values] : [...state.values, value]

      initSets(sets, page)
      initValues(sets, values, page)

      return dispatch({type: CREATE_SET, values, sets})
    }

    if (isNil(value)) {
      return action()
    } else {
      return dispatch(storeValue(value)).then((value) => action(value))
    }
  }
}

export function updateSet(setValue, attrs) {
  return storeValue(ValueFactory.update(setValue, attrs))
}

export function deleteSet(set, setValue) {
  if (isNil(setValue)) {
    return (dispatch, getState) => {
      // gather all values for this set and it's descendants
      const values = getDescendants(getState().interview.values, set)

      return Promise.all(values.map((value) => ValueApi.deleteValue(projectId, value)))
        .then(() => dispatch(deleteSetSuccess(set)))
        .catch((errors) => dispatch(deleteValueError(errors)))
    }
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

  return (dispatch, getState) => {
    // again, gather all values for this set and it's descendants
    const sets = [...getDescendants(getState().interview.sets, set), set]
    const values = getDescendants(getState().interview.values, set)
    return dispatch({type: DELETE_SET_SUCCESS, sets, values})
  }
}

export function deleteSetError(errors) {
  return {type: DELETE_SET_ERROR, errors}
}
