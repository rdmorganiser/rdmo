import { first, isEmpty, isNil } from 'lodash'

import PageApi from '../api/PageApi'
import ProjectApi from '../api/ProjectApi'
import ValueApi from '../api/ValueApi'

import { elementTypes } from 'rdmo/management/assets/js/constants/elements'

import { updateProgress } from './projectActions'

import { updateLocation } from '../utils/location'

import { updateOptions } from '../utils/options'
import { initPage } from '../utils/page'
import { copyResolvedConditions, getDescendants, gatherSets, initSets } from '../utils/set'
import { gatherDefaultValues, initValues, compareValues, isEmptyValue } from '../utils/value'
import { projectId } from '../utils/meta'

import ValueFactory from '../factories/ValueFactory'
import SetFactory from '../factories/SetFactory'

import {
  NOOP,
  FETCH_PAGE_INIT,
  FETCH_PAGE_SUCCESS,
  FETCH_PAGE_ERROR,
  FETCH_NAVIGATION_INIT,
  FETCH_NAVIGATION_SUCCESS,
  FETCH_NAVIGATION_ERROR,
  FETCH_OPTIONS_INIT,
  FETCH_OPTIONS_SUCCESS,
  FETCH_OPTIONS_ERROR,
  FETCH_VALUES_INIT,
  FETCH_VALUES_SUCCESS,
  FETCH_VALUES_ERROR,
  RESOLVE_CONDITION_INIT,
  RESOLVE_CONDITION_SUCCESS,
  RESOLVE_CONDITION_ERROR,
  CREATE_VALUE,
  UPDATE_VALUE,
  STORE_VALUE_INIT,
  STORE_VALUE_SUCCESS,
  STORE_VALUE_ERROR,
  DELETE_VALUE_INIT,
  DELETE_VALUE_SUCCESS,
  DELETE_VALUE_ERROR,
  CREATE_SET,
  DELETE_SET_INIT,
  DELETE_SET_SUCCESS,
  DELETE_SET_ERROR,
  COPY_SET_INIT,
  COPY_SET_SUCCESS,
  COPY_SET_ERROR
} from './actionTypes'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

export function fetchPage(pageId, back) {
  const pendingId = 'fetchPage'

  return (dispatch, getState) => {
    // store unsaved defaults on this page before loading the new page
    gatherDefaultValues(getState().interview.page, getState().interview.values).forEach((value) => {
      ValueApi.storeValue(projectId, value)
    })

    dispatch(addToPending(pendingId))
    dispatch(fetchPageInit())

    if (pageId === 'done') {
      updateLocation('done')
      dispatch(fetchNavigation(null))
      dispatch(fetchPageSuccess(null, true))
      dispatch(removeFromPending(pendingId))
    } else {
      const promise = isNil(pageId) ? PageApi.fetchContinue(projectId)
                                    : PageApi.fetchPage(projectId, pageId, back)
      return promise
        .then((page) => {
          updateLocation(page.id)

          initPage(page)

          dispatch(fetchNavigation(page))
          dispatch(fetchValues(page))
          dispatch(fetchOptionsets(page))

          dispatch(removeFromPending(pendingId))
          dispatch(fetchPageSuccess(page, false))
        })
        .catch((error) => {
          dispatch(removeFromPending(pendingId))
          if (error.errors.done) {
            dispatch(fetchPage('done'))
          } else {
            dispatch(fetchPageError(error))
          }
        })
    }
  }
}

export function fetchPageInit() {
  return {type: FETCH_PAGE_INIT}
}

export function fetchPageSuccess(page, done) {
  return {type: FETCH_PAGE_SUCCESS, page, done}
}

export function fetchPageError(error) {
  return {type: FETCH_PAGE_ERROR, error}
}

export function fetchNavigation(page) {
  const pendingId = `fetchNavigation/${page ? page.id : 'done'}`

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(fetchNavigationInit())

    return ProjectApi.fetchNavigation(projectId, page && page.section.id)
      .then((navigation) => {
        dispatch(removeFromPending(pendingId))
        dispatch(fetchNavigationSuccess(navigation))
      })
      .catch((error) => {
        dispatch(removeFromPending(pendingId))
        dispatch(fetchNavigationError(error))
      })
  }
}

export function fetchNavigationInit() {
  return {type: FETCH_NAVIGATION_INIT}
}

export function fetchNavigationSuccess(navigation) {
  return {type: FETCH_NAVIGATION_SUCCESS, navigation}
}

export function fetchNavigationError(error) {
  return {type: FETCH_NAVIGATION_ERROR, error}
}

export function fetchOptionsets(page) {
  return (dispatch) => {
    page.optionsets.filter((optionset) => (optionset.has_provider && !optionset.has_search))
                   .forEach((optionset) => dispatch(fetchOptions(page, optionset)))
  }
}

export function fetchOptions(page, optionset) {
  const pendingId = `fetchOptions/${page.id}/${optionset.id}`

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(fetchOptionsInit())

    return ProjectApi.fetchOptions(projectId, optionset.id)
      .then((options) => {
        updateOptions(page, optionset, options)

        dispatch(removeFromPending(pendingId))
        dispatch(fetchOptionsSuccess(page, optionset, options))
      })
      .catch((error) => {
        dispatch(removeFromPending(pendingId))
        dispatch(fetchOptionsError(error))
      })
  }
}

export function fetchOptionsInit() {
  return {type: FETCH_OPTIONS_INIT}
}

export function fetchOptionsSuccess(page) {
  return {type: FETCH_OPTIONS_SUCCESS, page}
}

export function fetchOptionsError(error) {
  return {type: FETCH_OPTIONS_ERROR, error}
}

export function fetchValues(page) {
  const pendingId = `fetchValues/${page.id}`

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(fetchValuesInit())
    return ValueApi.fetchValues(projectId, { attribute: page.attributes })
      .then((values) => {
        const sets = gatherSets(values, page)

        initSets(sets, page)
        initValues(sets, values, page)

        dispatch(removeFromPending(pendingId))
        dispatch(resolveConditions(page, sets))
        dispatch(fetchValuesSuccess(values, sets))
      })
      .catch((error) => {
        dispatch(removeFromPending(pendingId))
        dispatch(fetchValuesError(error))
      })
  }
}

export function fetchValuesInit() {
  return {type: FETCH_VALUES_INIT}
}

export function fetchValuesSuccess(values, sets) {
  return {type: FETCH_VALUES_SUCCESS, values, sets}
}

export function fetchValuesError(error) {
  return {type: FETCH_VALUES_ERROR, error}
}

export function resolveConditions(page, sets) {
  return (dispatch) => {
    // loop over set to evaluate conditions
    sets.forEach((set) => {
      page.questionsets.filter((questionset) => questionset.has_conditions)
                       .forEach((questionset) => dispatch(resolveCondition(questionset, set)))

      page.questions.filter((question) => question.has_conditions)
                    .forEach((question) => dispatch(resolveCondition(question, set)))

      page.optionsets.filter((optionset) => optionset.has_conditions)
                     .forEach((optionset) => dispatch(resolveCondition(optionset, set)))
    })
  }
}

export function resolveCondition(element, set) {
  const pendingId = `resolveCondition/${element.model}/${element.id}/${set.set_prefix}/${set.set_index}`

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(resolveConditionInit())

    return ProjectApi.resolveCondition(projectId, set, element)
      .then((response) => {
        const elementType = elementTypes[element.model]
        dispatch(removeFromPending(pendingId))
        dispatch(resolveConditionSuccess(set, elementType, element.id, response.result))
      })
      .catch((error) => {
        dispatch(removeFromPending(pendingId))
        dispatch(resolveConditionError(error))
      })
  }
}

export function resolveConditionInit() {
  return {type: RESOLVE_CONDITION_INIT}
}

export function resolveConditionSuccess(set, elementType, elementId, result) {
  return {type: RESOLVE_CONDITION_SUCCESS, set, elementType, elementId, result}
}

export function resolveConditionError(error) {
  return {type: RESOLVE_CONDITION_ERROR, error}
}

export function storeValue(value) {
  const pendingId = `storeValue/${value.attribute}/${value.set_prefix}/${value.set_index}/${value.collection_index}`

  if (value.pending) {
    return {type: NOOP}
  } else {
    return (dispatch, getState) => {
      const page = getState().interview.page
      const sets = getState().interview.sets
      const question = page.questions.find((question) => question.attribute === value.attribute)
      const refresh = question && question.optionsets.some((optionset) => optionset.has_refresh)
      const widget_type = question && question.widget_type

      const valueIndex = getState().interview.values.findIndex((v) => compareValues(v, value, widget_type))
      const valueText = value.text
      const valueFile = value.file
      const valueSuccess = value.success

      dispatch(addToPending(pendingId))
      dispatch(storeValueInit(valueIndex))

      return ValueApi.storeValue(projectId, { ...value, widget_type })
        .then((value) => {

          dispatch(fetchNavigation(page))
          dispatch(updateProgress())

          if (refresh) {
            // if the refresh flag is set, reload all values for the page,
            // resolveConditions will be called in fetchValues
            dispatch(fetchValues(page))
          } else {
            dispatch(resolveConditions(page, sets))
          }

          // set the success flag and start the timeout to remove it. the flag is actually
          // the stored timeout, so we can cancel any old timeout before starting the a new
          // one in order to prolong the time the indicator is show with each save
          clearTimeout(valueSuccess)
          value.success = setTimeout(() => {
            dispatch(updateValue(value, {success: false}, false))
          }, 1000)

          // replace the text with the old text if it was trimmed by the backend
          // (but not if a new text was inserted, e.g. by an optionset provider)
          if (valueText.trim() == value.text) {
            value.text = valueText
          }

          // check if there is a file or if a filename is set (when the file was just erased)
          if (isNil(valueFile) && isNil(value.file_name)) {
            dispatch(removeFromPending(pendingId))
            dispatch(storeValueSuccess(value, valueIndex))
          } else {
            // upload file after the value is created
            return ValueApi.storeFile(projectId, value, valueFile)
              .then((value) => {
                dispatch(removeFromPending(pendingId))
                dispatch(storeValueSuccess(value, valueIndex))
              })
              .catch((error) => {
                dispatch(removeFromPending(pendingId))
                dispatch(storeValueError(error, valueIndex))
              })
          }
        })
        .catch((error) => {
          dispatch(removeFromPending(pendingId))
          dispatch(storeValueError(error, valueIndex))
        })
    }
  }
}

export function storeValueInit(valueIndex) {
  return {type: STORE_VALUE_INIT, valueIndex}
}

export function storeValueSuccess(value, valueIndex) {
  return {type: STORE_VALUE_SUCCESS, value, valueIndex}
}

export function storeValueError(error, valueIndex) {
  return {type: STORE_VALUE_ERROR, error, valueIndex}
}

export function createValue(attrs, store) {
  const value = ValueFactory.create(attrs)

  // focus the new value
  value.focus = true

  if (isNil(store)) {
    return {type: CREATE_VALUE, value}
  } else {
    return storeValue(value)
  }
}

export function updateValue(value, attrs, store = true) {
  if (store) {
    return storeValue(ValueFactory.update(value, attrs))
  } else {
     return {type: UPDATE_VALUE, value, attrs}
  }
}

export function copyValue(question, ...originalValues) {
  const firstValue = first(originalValues)
  const pendingId = `copyValue/${firstValue.attribute}/${firstValue.set_prefix}/${firstValue.set_index}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))

    const { sets, values } = getState().interview

    // create copies for each value for all it's empty siblings
    const copies = originalValues.reduce((copies, value) => {
      return [
        ...copies,
        ...sets.filter((set) => (
          (set.set_prefix == value.set_prefix) &&
          (set.set_index != value.set_index) &&
          (set.element == question.parent)
        )).map((set) => {
          // check if every sibling is empty
          if (values.filter((v) => (
            (v.attribute == value.attribute) &&
            (v.set_prefix == set.set_prefix) &&
            (v.set_index == set.set_index)
          )).every(v => isEmptyValue(v))) {
            // find the corresponding sibling to this original value
            const siblingIndex = values.findIndex((v) => (
              (v.attribute == value.attribute) &&
              (v.set_prefix == set.set_prefix) &&
              (v.set_index == set.set_index) &&
              (v.collection_index == value.collection_index)
            ))

            const sibling = siblingIndex > 0 ? values[siblingIndex] : null

            if (isNil(sibling)) {
              return [ValueFactory.create({ ...value, set_index: set.set_index }), siblingIndex]
            } else if (isEmptyValue(sibling)) {
              // the spread operator { ...sibling } does prevent an update in place
              return [ValueFactory.update({ ...sibling }, value), siblingIndex]
            } else {
              return null
            }
          } else {
            return null
          }
        }).filter((value) => !isNil(value))
      ]
    }, [])

    // dispatch storeValueInit for each of the updated values,
    // created values have valueIndex -1 and will be skipped
    // eslint-disable-next-line no-unused-vars
    copies.forEach(([value, valueIndex]) => dispatch(storeValueInit(valueIndex)))

    // loop over all copies and store the values on the server
    // afterwards fetchNavigation, updateProgress and check refresh once
    return Promise.all(
      copies.map(([value, valueIndex]) => {
        return ValueApi.storeValue(projectId, value)
          .then((value) => dispatch(storeValueSuccess(value, valueIndex)))
      })
    ).then(() => {
      dispatch(removeFromPending(pendingId))

      const page = getState().interview.page
      const sets = getState().interview.sets
      const question = page.questions.find((question) => question.attribute === firstValue.attribute)
      const refresh = question && question.optionsets.some((optionset) => optionset.has_refresh)

      dispatch(fetchNavigation(page))
      dispatch(updateProgress())

      if (refresh) {
        // if the refresh flag is set, reload all values for the page,
        // resolveConditions will be called in fetchValues
        dispatch(fetchValues(page))
      } else {
        dispatch(resolveConditions(page, sets))
      }
    })
  }
}

export function deleteValue(value) {
  const pendingId = `deleteValue/${value.id}`

  if (value.pending) {
    return {type: NOOP}
  } else {
    return (dispatch, getState) => {
      dispatch(addToPending(pendingId))
      dispatch(deleteValueInit(value))

      if (isNil(value.id)) {
        return dispatch(deleteValueSuccess(value))
      } else {
        return ValueApi.deleteValue(projectId, value)
          .then(() => {
            const page = getState().interview.page
            const sets = getState().interview.sets
            const question = page.questions.find((question) => question.attribute === value.attribute)
            const refresh = question.optionsets.some((optionset) => optionset.has_refresh)

            dispatch(fetchNavigation(page))
            dispatch(updateProgress())

            if (refresh) {
              // if the refresh flag is set, reload all values for the page,
              // resolveConditions will be called in fetchValues
              dispatch(fetchValues(page))
            } else {
              dispatch(resolveConditions(page, sets))
            }

            dispatch(removeFromPending(pendingId))
            dispatch(deleteValueSuccess(value))
          })
          .catch((errors) => {
            dispatch(removeFromPending(pendingId))
            dispatch(deleteValueError(errors))
          })
      }
    }
  }
}

export function deleteValueInit(value) {
  return {type: DELETE_VALUE_INIT, value}
}

export function deleteValueSuccess(value) {
  return {type: DELETE_VALUE_SUCCESS, value}
}

export function deleteValueError(errors) {
  return {type: DELETE_VALUE_ERROR, errors}
}

export function activateSet(set) {
  if (isEmpty(set.set_prefix)) {
    return updateConfig('page.currentSetIndex', set.set_index)
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

    // create a callback function to be called immediately or after saving the value
    const createSetCallback = (value) => {
      dispatch(activateSet(set))

      const state = getState().interview
      const page = state.page
      const sets = [...state.sets, set]
      const values = isNil(value) ? [...state.values] : [...state.values, value]

      initSets(sets, page)
      initValues(sets, values, page)

      dispatch(resolveConditions(page, sets))

      return dispatch({type: CREATE_SET, values, sets})
    }

    if (isNil(value)) {
      return createSetCallback()
    } else {
      return dispatch(storeValue(value)).then(() => {
        const storedValue = getState().interview.values.find((v) => compareValues(v, value))
        if (!isNil(storedValue)) {
          createSetCallback(storedValue)
        }
      })
    }
  }
}

export function updateSet(setValue, attrs) {
  return storeValue(ValueFactory.update(setValue, attrs))
}

export function deleteSet(set, setValue) {
  const pendingId = `deleteSet/${set.set_prefix}/${set.set_index}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(deleteSetInit())

    if (isNil(setValue)) {
      // gather all values for this set and it's descendants
      const { values } = getDescendants(getState().interview.values, getState().interview.sets, set)

      return Promise.all(values.map((value) => ValueApi.deleteValue(projectId, value)))
        .then(() => {
          dispatch(removeFromPending(pendingId))
          dispatch(updateProgress())
          dispatch(deleteSetSuccess(set))
        })
        .catch((errors) => {
          dispatch(removeFromPending(pendingId))
          dispatch(deleteSetError(errors))
        })
    } else {
      return ValueApi.deleteSet(projectId, setValue)
        .then(() => {
          const page = getState().interview.page

          dispatch(fetchNavigation(page))
          dispatch(updateProgress())

          const sets = getState().interview.sets.filter((s) => (s.set_prefix == set.set_prefix))

          if (sets.length > 1) {
            const index = sets.indexOf(set)
            if (index < sets.length - 1) {
              dispatch(activateSet(sets[index + 1]))
            } else {
              // If it's the last set, activate the new last set
              dispatch(activateSet(sets[index - 1]))
            }
          }

          dispatch(removeFromPending(pendingId))
          dispatch(deleteSetSuccess(set))
        })
        .catch((errors) => {
          dispatch(removeFromPending(pendingId))
          dispatch(deleteSetError(errors))
        })
    }
  }
}

export function deleteSetInit() {
  return {type: DELETE_SET_INIT}
}

export function deleteSetSuccess(set) {
  return (dispatch, getState) => {
    // again, gather all values for this set and it's descendants
    const { sets, values } = getDescendants(getState().interview.values, getState().interview.sets, set)

    return dispatch({type: DELETE_SET_SUCCESS, sets, values})
  }
}

export function deleteSetError(errors) {
  return {type: DELETE_SET_ERROR, errors}
}

export function copySet(currentSet, copySetValue, attrs) {
  const pendingId = isNil(currentSet) ? 'copySet' : `copySet/${currentSet.set_prefix}/${currentSet.set_index}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(copySetInit())

    // create a new set (create) or use the current one (import)
    const set = isNil(attrs.id) ? SetFactory.create(attrs) : currentSet

    // create a value for the text if the page has an attribute (create) or use the current one (import)
    const value = isNil(attrs.attribute) ? null : (
      isNil(attrs.id) ? ValueFactory.create(attrs) : attrs
    )

    // create a callback function to be called immediately or after saving the value
    const copySetCallbackAction = (setValues) => {
      dispatch(activateSet(set))

      const state = getState().interview

      const page = state.page
      const values = [
        ...state.values.filter(v => !setValues.some(sv => compareValues(v, sv))),  // remove updated values
        ...setValues
      ]
      const sets = gatherSets(values, page)

      initSets(sets, page)
      initValues(sets, values, page)

      // copy already resolved conditions to prevent short hiding of questions
      copyResolvedConditions(state.sets, sets)

      dispatch(resolveConditions(page, sets))
      dispatch({type: COPY_SET_SUCCESS, values, sets})
    }

    let promise
    if (isNil(value)) {
      // gather all values for the currentSet and it's descendants
      const { values: currentValues } = getDescendants(getState().interview.values,
                                                       getState().interview.sets, currentSet)

      // store each value in currentSet with the new set_index
      promise = Promise.all(
        currentValues.filter((currentValue) => !isEmptyValue(currentValue)).map((currentValue) => {
          const value = {...currentValue}
          const setPrefixLength = isEmpty(set.set_prefix) ? 0 : set.set_prefix.split('|').length

          if (value.set_prefix == set.set_prefix) {
            value.set_index = set.set_index
          } else {
            value.set_prefix = value.set_prefix.split('|').map((sp, idx) => {
              // for the set_prefix of the new value, set the number at the position, which is one more
              // than the length of the set_prefix of the new (and old) set, to the set_index of the new set.
              // since idx counts from 0, this equals setPrefixLength
              return (idx == setPrefixLength) ? set.set_index : sp
            }).join('|')
          }

          delete value.id
          return ValueApi.storeValue(projectId, value)
        })
      )
    } else {
      promise = ValueApi.copySet(projectId, value, copySetValue)
    }

    return promise.then((values) => {
      dispatch(removeFromPending(pendingId))
      copySetCallbackAction(values)
    }).catch((errors) => {
      dispatch(removeFromPending(pendingId))
      dispatch(copySetError(errors))
    })
  }
}

export function copySetInit() {
  return {type: COPY_SET_INIT}
}

export function copySetSuccess(values, sets) {
  return {type: COPY_SET_SUCCESS, values, sets}
}

export function copySetError(errors) {
  return {type: COPY_SET_ERROR, errors}
}
