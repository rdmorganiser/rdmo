import { first, isEmpty, isNil, omit, uniqueId } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { clearError, setError } from 'rdmo/core/assets/js/actions/errorsActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { selectReadOnly } from '../../common/selectors/permissions'
import { actions } from '../reducers/interviewSlice'
import { projectId } from '../utils/meta'
import { initPage } from '../utils/page'
import { copyResolvedConditions, gatherSets, getDescendants, initSets } from '../utils/set'
import {
  compareValueId,
  compareValues,
  gatherDefaultValues,
  initValues,
  isEmptyValue,
  sortValues
} from '../utils/value'

import PageApi from '../api/PageApi'
import ProjectApi from '../api/ProjectApi'
import ValueApi from '../api/ValueApi'
import SetFactory from '../factories/SetFactory'
import ValueFactory from '../factories/ValueFactory'

import { fetchNavigation, fetchProgress, updateProgress } from './projectActions'

// Only requests and Files live here; the latest value content stays in Redux.
const valueSaveRequests = {}

const getCurrentValue = (getState, value) => getState().interview.values?.find(currentValue => (
  compareValueId(currentValue, value.tmp_id || value.id)
))

export function fetchPage(pageId, back) {
  const pendingId = 'fetchPage'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(fetchProgress())
    dispatch(fetchNavigation())
    dispatch(actions.fetchPageInit())
    dispatch(clearError('page', 'continue', 'options', 'conditions', 'copyValue', 'deleteSet', 'copySet'))

    return PageApi.fetchPage(projectId, pageId, back)
      .then((page) => {
        initPage(page)
        Object.entries(valueSaveRequests).forEach(([key, request]) => {
          if (!request.promise) delete valueSaveRequests[key]
        })

        dispatch(fetchValues(page))
        dispatch(fetchOptionsets(page))

        dispatch(actions.fetchPageSuccess({ page }))

        // return the page, so that navigateDashboard can update the location accordingly
        return page
      })
      .catch((error) => {
        if (error?.errors?.done) {
          dispatch(showDone())
        } else {
          dispatch(setError('page', error, gettext('Page')))
        }
      })
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchContinue() {
  const pendingId = 'fetchContinue'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(clearError('continue'))

    return PageApi.fetchContinue(projectId)
      .then((page) => dispatch(actions.fetchContinueSuccess(page)))
      .catch((error) => dispatch(setError('continue', error, gettext('Continue'))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
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
    dispatch(clearError('options'))

    return ProjectApi.fetchOptions(projectId, optionset.id)
      .then((options) => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchOptionsSuccess({ pageId: page.id, optionsetId: optionset.id, options }))
      })
      .catch((error) => dispatch(setError('options', error, gettext('Options'))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchValues(page, refresh = false) {
  const requestId = uniqueId('fetchValues_')
  const pendingId = `fetchValues/${page.id}/${requestId}`

  return (dispatch, getState) => {
    const originalValues = getState().interview.values || []
    dispatch(addToPending(pendingId))
    dispatch(clearError('values'))
    dispatch(actions.fetchValuesInit(requestId))

    return ValueApi.fetchValues(projectId, { attribute: page.attributes })
      .then((values) => {
        const state = getState().interview
        if (state.page !== page || state.valuesRequestId !== requestId) return

        if (refresh) {
          const currentValues = state.values
          values = values.flatMap(value => {
            const originalValue = originalValues.find(currentValue => compareValues(currentValue, value))
            const currentValue = currentValues.find(currentValue => compareValues(currentValue, value))
            // Do not restore an answer removed while the refresh was running.
            if (originalValue && !currentValue) return []
            if (!currentValue) return [value]

            const changed = !originalValue ||
              currentValue.revision !== originalValue.revision || currentValue.updated !== originalValue.updated
            const unsaved = (currentValue.revision || 0) !== (currentValue.savedRevision || 0)
            if (changed || unsaved || currentValue.pending || currentValue.error) return [currentValue]

            // Server/plugin changes apply to clean values, retaining their local identity and indicators.
            return [{ ...currentValue, ...value }]
          })

          const keptValues = currentValues.filter(value => (
            (isNil(value.id) || value.pending || value.error ||
              (value.revision || 0) !== (value.savedRevision || 0) ||
              !originalValues.some(originalValue => (
                compareValues(originalValue, value) && originalValue.revision === value.revision &&
                originalValue.updated === value.updated
              ))) && !values.some(currentValue => compareValues(currentValue, value))
          ))
          values = sortValues([...values, ...keptValues])
        }

        const sets = gatherSets(values, page)
        initSets(sets, page)
        initValues(sets, values, page)
        if (refresh) copyResolvedConditions(state.sets, sets)

        dispatch(actions.fetchValuesSuccess({ values, sets }))
        return dispatch(resolveConditions(page, sets))
      })
      .catch((error) => {
        const state = getState().interview
        if (state.page === page && state.valuesRequestId === requestId) {
          dispatch(setError('values', error, gettext('Values')))
        }
      })
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function resolveConditions(page, sets) {
  const pendingId = uniqueId('resolveConditions/')

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(clearError('conditions'))

    // loop over sets to gather payload
    const payload = []

    sets.forEach((set) => {
      page.questionsets
        .filter((questionset) => questionset.has_conditions)
        .forEach((questionset) => payload.push({
          element_type: 'questionsets',
          element_id: questionset.id,
          set_prefix: set.set_prefix,
          set_index: set.set_index,
        }))

      page.questions
        .filter((question) => question.has_conditions)
        .forEach((question) => payload.push({
          element_type: 'questions',
          element_id: question.id,
          set_prefix: set.set_prefix,
          set_index: set.set_index,
        }))

      page.optionsets
        .filter((optionset) => optionset.has_conditions)
        .forEach((optionset) => payload.push({
          element_type: 'optionsets',
          element_id: optionset.id,
          set_prefix: set.set_prefix,
          set_index: set.set_index,
        }))
    })

    return ProjectApi.resolveConditions(projectId, payload)
      .then((results) => {
        const state = getState().interview
        if (state.page === page && state.sets === sets) dispatch(actions.resolveConditionsSuccess(results))
      })
      .catch((error) => {
        if (getState().interview.page === page) {
          dispatch(setError('conditions', error, gettext('Conditions')))
        }
      })
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function storeValue(value, updatePage = true) {
  const valueId = value.tmp_id || value.id
  if (isNil(valueId)) {
    throw new Error('Could not determine valueId in storeValue')
  }

  return (dispatch, getState) => {
    const { page } = getState().interview
    const existingValue = getCurrentValue(getState, value)
    const key = `${page.id}/${existingValue?.tmp_id || existingValue?.id || valueId}`
    const previous = valueSaveRequests[key]
    const request = previous?.page === page ? previous : { page }
    // A pending delete must not start an overlapping save.
    if (existingValue?.pending && !request.promise) return Promise.resolve(dispatch(actions.noop()))
    valueSaveRequests[key] = request
    request.updatePage = request.updatePage || updatePage
    if ('file' in value) request.file = value.file
    if (request.promise) return request.promise

    const pendingId = uniqueId(`storeValue/${key}/`)
    const question = page.questions.find(question => question.attribute === value.attribute)
    const refresh = question && question.optionsets.some(optionset => optionset.has_refresh)
    const widget_type = question && question.widget_type
    let succeeded = false

    const storeNextValue = async () => {
      let currentValue = getCurrentValue(getState, value) || value
      while (currentValue && getState().interview.page === page) {
        const revision = currentValue.revision || 0
        const valueText = currentValue.text
        const valueFile = request.file
        clearTimeout(currentValue.success)
        dispatch(actions.storeValueInit(currentValue.id || currentValue.tmp_id))

        let storedValue = await ValueApi.storeValue(projectId, { ...currentValue, widget_type })
        // Finish the upload even if navigation has already changed the visible page.
        // Keep the server identity even if the subsequent upload fails.
        if (getState().interview.page === page) {
          if (getCurrentValue(getState, value)) {
            dispatch(actions.storeValueMetadata({ value: storedValue, valueId }))
          } else if (!existingValue && isNil(currentValue.id)) {
            // New answers become visible after creation, with their temporary identity retained.
            dispatch(actions.createValue({ ...omit(value, 'file'), ...storedValue, pending: true }))
          }
        }
        if (!isNil(valueFile) || !isNil(storedValue.file_name)) {
          storedValue = await ValueApi.storeFile(projectId, storedValue, valueFile)
        }
        if (getState().interview.page !== page || !getCurrentValue(getState, value)) return

        // Preserve whitespace trimmed by the backend, but accept provider-generated text.
        if (valueText.trim() == storedValue.text) storedValue.text = valueText
        currentValue = getCurrentValue(getState, value)
        const pending = (currentValue.revision || 0) !== revision
        if (!pending && request.updatePage) {
          storedValue.success = setTimeout(() => {
            if (getState().interview.page === page) {
              dispatch(updateValue(storedValue, { success: false }, false))
            }
          }, 1000)
        }
        dispatch(actions.storeValueSuccess({ value: storedValue, valueId, revision }))
        if (!pending) {
          succeeded = true
          return
        }
        currentValue = getCurrentValue(getState, value)
      }
    }

    request.promise = Promise.resolve()
      .then(storeNextValue)
      .catch((error) => {
        if (getState().interview.page === page) {
          dispatch(actions.storeValueError({ error: serializeError(error), valueId }))
        }
      })
      .finally(() => {
        request.promise = null
        // Retain a failed upload's latest File for the next save attempt, outside Redux.
        if (valueSaveRequests[key] === request &&
            (succeeded || isNil(request.file) || getState().interview.page !== page)) {
          delete valueSaveRequests[key]
        }
        dispatch(removeFromPending(pendingId))
      })
      .then(() => {
        if (!succeeded || !request.updatePage || getState().interview.page !== page) return
        dispatch(fetchNavigation())
        dispatch(updateProgress())
        if (refresh) {
          return dispatch(fetchValues(page, true))
        } else {
          return dispatch(resolveConditions(page, getState().interview.sets))
        }
      })

    dispatch(addToPending(pendingId))
    dispatch(actions.storeValueInit(existingValue?.id || valueId))
    return request.promise
  }
}

export function storeDefaultValues() {
  const pendingId = 'storeDefaultValues'

  return (dispatch, getState) => {
    const { page, values } = getState().interview

    // defaults are not stored for read-only users, since they cannot edit them
    if (selectReadOnly(getState())) {
      return Promise.resolve()
    }

    const pendingSaves = Object.values(valueSaveRequests)
      .filter(request => request.page === page && request.promise)
      .map(request => request.promise)
    const defaultValues = gatherDefaultValues(page, values).filter((value) => !value.pending)
    if (isEmpty(defaultValues) && isEmpty(pendingSaves)) {
      return Promise.resolve()
    }

    dispatch(addToPending(pendingId))

    // Navigation must also wait for edits already being saved, including their waiting revisions.
    return Promise.all([...pendingSaves, ...defaultValues.map(value => dispatch(storeValue(value, false)))])
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function createValue(attrs, store) {
  const value = ValueFactory.create(attrs)

  // focus the new value
  value.focus = true

  if (isNil(store)) {
    return actions.createValue(omit(value, 'file'))
  } else {
    return storeValue(value)
  }
}

export function updateValue(value, attrs, store = true) {
  if (store) {
    return (dispatch, getState) => {
      const currentValue = getCurrentValue(getState, value)
      // A delayed callback must not recreate an answer removed or left behind by navigation.
      if (!currentValue || !getState().interview.page.attributes.includes(currentValue.attribute)) {
        return dispatch(actions.noop())
      }
      clearTimeout(currentValue.success)
      const valueToSave = ValueFactory.update({ ...currentValue }, attrs)
      const valueForState = omit(valueToSave, 'file')
      dispatch(actions.updateValue({ value: currentValue, attrs: valueForState, store: true }))
      return dispatch(storeValue(valueToSave))
    }
  } else {
    return actions.updateValue({ value, attrs })
  }
}

export function copyValue(question, ...originalValues) {
  const valuesToCopy = originalValues.filter((v) => !isEmptyValue(v))

  const firstValue = first(valuesToCopy)

  if (isNil(firstValue)) {
    return actions.noop()
  }

  const pendingId = `copyValue/${firstValue.attribute}/${firstValue.set_prefix}/${firstValue.set_index}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(clearError('copyValue'))

    const { page, sets, values } = getState().interview

    // create copies for each value for all it's empty siblings
    const copies = valuesToCopy.reduce((copies, value) => {
      return [
        ...copies,
        ...sets.filter((set) => (
          (set.set_prefix == value.set_prefix) &&
          (set.set_index != value.set_index) &&
          (set.element.elements.includes(question))
        )).map((set) => {
          // check if every sibling is empty
          if (values.filter((v) => (
            (v.attribute == value.attribute) &&
            (v.set_prefix == set.set_prefix) &&
            (v.set_index == set.set_index)
          )).every(v => isEmptyValue(v))) {
            // find the corresponding sibling to this original value
            const sibling = values.find((v) => (
              (v.attribute == value.attribute) &&
              (v.set_prefix == set.set_prefix) &&
              (v.set_index == set.set_index) &&
              (v.collection_index == value.collection_index)
            ))

            if (isNil(sibling)) {
              return [ValueFactory.create({ ...value, set_index: set.set_index }), null]
            } else if (isEmptyValue(sibling)) {
              // the spread operator { ...sibling } does prevent an update in place
              return [ValueFactory.update({ ...sibling }, value), sibling.id || sibling.tmp_id]
            } else {
              return null
            }
          } else {
            return null
          }
        }).filter((value) => !isNil(value))
      ]
    }, [])

    // Use the same save handling as edits, then refresh the page once for all copies.
    return Promise.all(copies.map(([value, valueId]) => {
      if (!isNil(valueId)) {
        dispatch(actions.updateValue({ value, attrs: omit(value, 'file'), store: true }))
      }
      return dispatch(storeValue(value, false))
    })).then(() => {
      if (getState().interview.page !== page) return
      // sort values in the store after the updates
      dispatch(resortValues())

      const sets = getState().interview.sets
      const question = page.questions.find((question) => question.attribute === firstValue.attribute)
      const refresh = question && question.optionsets.some((optionset) => optionset.has_refresh)

      dispatch(fetchNavigation())
      dispatch(updateProgress())

      if (refresh) {
        // if the refresh flag is set, reload all values for the page,
        // resolveConditions will be called in fetchValues. Preserve unsaved values,
        // since they are not included in the response from the backend.
        return dispatch(fetchValues(page, true))
      } else {
        return dispatch(resolveConditions(page, sets))
      }
    })
      .catch((error) => dispatch(setError('copyValue', error, gettext('Copy value'))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function deleteValue(value) {
  const valueId = value.id || value.tmp_id
  if (isNil(valueId)) {
    throw new Error('Could not determine valueId in deleteValue')
  }

  const pendingId = `deleteValue/${valueId}`

  if (value.pending) {
    return actions.noop()
  } else {
    return (dispatch, getState) => {
      dispatch(addToPending(pendingId))
      dispatch(actions.deleteValueInit(valueId))

      if (isNil(value.id)) {
        dispatch(removeFromPending(pendingId))
        return dispatch(actions.deleteValueSuccess(valueId))
      } else {
        return ValueApi.deleteValue(projectId, value)
          .then(() => {
            const page = getState().interview.page
            const sets = getState().interview.sets
            const question = page.questions.find((question) => question.attribute === value.attribute)
            const refresh = question.optionsets.some((optionset) => optionset.has_refresh)

            dispatch(fetchNavigation())
            dispatch(updateProgress())

            if (refresh) {
              // if the refresh flag is set, reload all values for the page,
              // resolveConditions will be called in fetchValues. Preserve unsaved values,
              // since they are not included in the response from the backend.
              dispatch(fetchValues(page, true))
            } else {
              dispatch(resolveConditions(page, sets))
            }

            dispatch(actions.deleteValueSuccess(valueId))
          })
          .catch((error) => dispatch(actions.deleteValueError({ error: serializeError(error), valueId })))
          .finally(() => dispatch(removeFromPending(pendingId)))
      }
    }
  }
}

export function activateSet(set) {
  if (isEmpty(set.set_prefix)) {
    return updateConfig('page.currentSetIndex', set.set_index)
  } else {
    return actions.noop()
  }
}

export function createSet(attrs) {
  return (dispatch, getState) => {
    const page = getState().interview.page
    // create a new set
    const set = SetFactory.create(attrs)

    // create a value for the text if the page has an attribute
    const value = isNil(attrs.attribute) ? null : ValueFactory.create(attrs)

    // create a callback function to be called immediately or after saving the value
    const createSetCallback = (value) => {
      dispatch(activateSet(set))

      const state = getState().interview
      const page = state.page
      const sets = [...state.sets]
      if (!sets.some(currentSet => (
        currentSet.element === set.element && currentSet.set_prefix === set.set_prefix &&
        currentSet.set_index === set.set_index
      ))) sets.push(set)
      const values = isNil(value) || state.values.includes(value) ? [...state.values] : [...state.values, value]

      initSets(sets, page)
      initValues(sets, values, page)

      dispatch(resolveConditions(page, sets))

      return dispatch(actions.createSet({ values, sets }))
    }

    if (isNil(value)) {
      return createSetCallback()
    } else {
      return dispatch(storeValue(value)).then(() => {
        if (getState().interview.page !== page) return
        const storedValue = getState().interview.values.find((v) => compareValues(v, value))
        if (!isNil(storedValue?.id) && !storedValue.error) {
          createSetCallback(storedValue)
        }
      })
    }
  }
}

export function updateSet(setValue, attrs) {
  return updateValue(setValue, attrs)
}

export function deleteSet(set, setValue) {
  const pendingId = `deleteSet/${set.set_prefix}/${set.set_index}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(clearError('deleteSet'))

    if (isNil(setValue)) {
      // gather all values for this set and it's descendants
      const { values } = getDescendants(getState().interview.values, getState().interview.sets, set)

      return Promise.all(values.map((value) => ValueApi.deleteValue(projectId, value)))
        .then(() => {
          dispatch(updateProgress())
          dispatch(deleteSetSuccess(set))
        })
        .catch((error) => dispatch(setError('deleteSet', error, gettext('Delete set'))))
        .finally(() => dispatch(removeFromPending(pendingId)))
    } else {
      return ValueApi.deleteSet(projectId, setValue)
        .then(() => {
          dispatch(fetchNavigation())
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

          dispatch(deleteSetSuccess(set))
        })
        .catch((error) => dispatch(setError('deleteSet', error, gettext('Delete set'))))
        .finally(() => dispatch(removeFromPending(pendingId)))
    }
  }
}

export function deleteSetSuccess(set) {
  return (dispatch, getState) => {
    // again, gather all values for this set and it's descendants
    const { sets, values } = getDescendants(getState().interview.values, getState().interview.sets, set)

    return dispatch(actions.deleteSetSuccess({ sets, values }))
  }
}

export function copySet(currentSet, copySetValue, attrs) {
  const pendingId = isNil(currentSet) ? 'copySet' : `copySet/${currentSet.set_prefix}/${currentSet.set_index}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(clearError('copySet'))

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
        // remove updated values, when importing into an existing set
        ...state.values.filter(v => !setValues.some(sv => compareValues(v, sv))),
        ...setValues
      ]
      const sets = gatherSets(values, page)

      initSets(sets, page)
      initValues(sets, values, page)

      // copy already resolved conditions to prevent short hiding of questions
      copyResolvedConditions(state.sets, sets)

      dispatch(resolveConditions(page, sets))
      dispatch(actions.copySetSuccess({ values, sets }))
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

    return promise
      .then((values) => {
        dispatch(removeFromPending(pendingId))
        copySetCallbackAction(values)
      })
      .catch((error) => dispatch(setError('copySet', error, gettext('Copy set'))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function resortValues() {
  return actions.resortValues()
}

export function showDone() {
  return actions.showDone()
}

export function hideDone() {
  return actions.hideDone()
}
