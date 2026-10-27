import { first, isEmpty, isNil, omit } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { combinePermissions, isReadOnly } from '../../common/utils/permissions'
import { actions } from '../reducers/interviewSlice'
import { projectId } from '../utils/meta'
import { initPage } from '../utils/page'
import { copyResolvedConditions, gatherSets, getDescendants, initSets } from '../utils/set'
import { compareValues, gatherDefaultValues, initValues, isEmptyValue, sortValues } from '../utils/value'

import PageApi from '../api/PageApi'
import ProjectApi from '../api/ProjectApi'
import ValueApi from '../api/ValueApi'
import SetFactory from '../factories/SetFactory'
import ValueFactory from '../factories/ValueFactory'

import { fetchNavigation, fetchProgress, updateProgress } from './projectActions'

export function fetchPage(pageId, back) {
  const pendingId = 'fetchPage'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(fetchProgress())
    dispatch(fetchNavigation())
    dispatch(actions.fetchPageInit())

    return PageApi.fetchPage(projectId, pageId, back)
      .then((page) => {
        initPage(page)

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
          dispatch(actions.fetchPageError(error))
        }
      })
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchContinue() {
  const pendingId = 'fetchContinue'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(actions.fetchContinueInit())

    return PageApi.fetchContinue(projectId)
      .then((page) => dispatch(actions.fetchContinueSuccess(page)))
      .catch((error) => dispatch(actions.fetchContinueError(error)))
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
    dispatch(actions.fetchOptionsInit())

    return ProjectApi.fetchOptions(projectId, optionset.id)
      .then((options) => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchOptionsSuccess({ pageId: page.id, optionsetId: optionset.id, options }))
      })
      .catch((error) => dispatch(actions.fetchOptionsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchValues(page, refresh = false) {
  const pendingId = `fetchValues/${page.id}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(actions.fetchValuesInit())

    return ValueApi.fetchValues(projectId, { attribute: page.attributes })
      .then((values) => {
        if (refresh) {
          // if the values are just refreshed after a value is stored or deleted, loop
          // over the existing values and add all temporary values which were not stored yet
          const unsavedValues = getState().interview.values.filter((value) => isNil(value.id))

          // extend values with all unsaved values, which are not found in values
          const keptUnsavedValues = unsavedValues.filter(
            (value) => isNil(values.find((v) => compareValues(v, value)))
          )

          // resort the values, to ensure the correct collection_index order
          values = sortValues([...values, ...keptUnsavedValues])
        }

        const sets = gatherSets(values, page)

        initSets(sets, page)
        initValues(sets, values, page)

        dispatch(resolveConditions(page, sets))
        dispatch(actions.fetchValuesSuccess({ values, sets }))
      })
      .catch((error) => dispatch(actions.fetchValuesError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function resolveConditions(page, sets) {
  const pendingId = 'resolveConditions'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(actions.resolveConditionsInit())

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
      .then((results) => dispatch(actions.resolveConditionsSuccess(results)))
      .catch((error) => dispatch(actions.resolveConditionsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function storeValue(value) {
  const valueId = value.id || value.tmp_id
  if (isNil(valueId)) {
    throw new Error('Could not determine valueId in storeValue')
  }

  const pendingId = `storeValue/${valueId}`

  if (value.pending) {
    return actions.noop()
  } else {
    return (dispatch, getState) => {
      const page = getState().interview.page
      const sets = getState().interview.sets
      const question = page.questions.find((question) => question.attribute === value.attribute)
      const refresh = question && question.optionsets.some((optionset) => optionset.has_refresh)
      const widget_type = question && question.widget_type

      const valueText = value.text
      const valueFile = value.file
      const valueSuccess = value.success

      dispatch(addToPending(pendingId))
      dispatch(actions.storeValueInit(valueId))

      return ValueApi.storeValue(projectId, { ...value, widget_type })
        .then((value) => {
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
            dispatch(actions.storeValueSuccess({ value, valueId }))
          } else {
            // upload file after the value is created
            return ValueApi.storeFile(projectId, value, valueFile)
              .then((value) => dispatch(actions.storeValueSuccess({ value, valueId })))
              .catch((error) => dispatch(actions.storeValueError({ error: serializeError(error), valueId })))
          }
        })
        .catch((error) => dispatch(actions.storeValueError({ error: serializeError(error), valueId })))
        .finally(() => dispatch(removeFromPending(pendingId)))
    }
  }
}

export function storeDefaultValues() {
  const pendingId = 'storeDefaultValues'

  return (dispatch, getState) => {
    const { page, values } = getState().interview

    // defaults are not stored for read-only users, since they cannot edit them
    const permissions = combinePermissions(
      getState().project.project?.project?.permissions,
      getState().user.currentUser?.permissions
    )
    if (isReadOnly(permissions)) {
      return Promise.resolve()
    }

    const defaultValues = gatherDefaultValues(page, values).filter((value) => !value.pending)
    if (isEmpty(defaultValues)) {
      return Promise.resolve()
    }

    dispatch(addToPending(pendingId))

    return Promise.all(defaultValues.map((value) => {
      const valueId = value.tmp_id

      dispatch(actions.storeValueInit(valueId))

      return ValueApi.storeValue(projectId, value)
        .then((value) => dispatch(actions.storeValueSuccess({ value, valueId })))
        .catch((error) => dispatch(actions.storeValueError({ error, valueId })))
    })).finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function createValue(attrs, store) {
  const value = ValueFactory.create(attrs)

  // focus the new value
  value.focus = true

  if (isNil(store)) {
    return actions.createValue(value)
  } else {
    return storeValue(value)
  }
}

export function updateValue(value, attrs, store = true) {
  if (store) {
    const valueToSave = ValueFactory.update({ ...value }, attrs)
    const valueForState = omit(valueToSave, 'file')

    return (dispatch) => {
      dispatch(actions.updateValue({ value, attrs: valueForState }))
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

    const { sets, values } = getState().interview

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

    // dispatch storeValueInit for each of the updated values,
    copies.forEach(([, valueId]) => dispatch(actions.storeValueInit(valueId)))

    // loop over all copies and store the values on the server
    // afterwards fetchNavigation, updateProgress and check refresh once
    return Promise.all(
      copies.map(([value, valueId]) => (
        ValueApi.storeValue(projectId, value)
          .then((storedValue) => dispatch(actions.storeValueSuccess({ value: storedValue, valueId })))
      ))
    ).then(() => {
      // sort values in the store after the updates
      dispatch(resortValues())

      dispatch(removeFromPending(pendingId))

      const page = getState().interview.page
      const sets = getState().interview.sets
      const question = page.questions.find((question) => question.attribute === firstValue.attribute)
      const refresh = question && question.optionsets.some((optionset) => optionset.has_refresh)

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
    })
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
          .catch((errors) => dispatch(actions.deleteValueError(errors)))
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

      return dispatch(actions.createSet({ values, sets }))
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
  return updateValue(setValue, attrs)
}

export function deleteSet(set, setValue) {
  const pendingId = `deleteSet/${set.set_prefix}/${set.set_index}`

  return (dispatch, getState) => {
    dispatch(addToPending(pendingId))
    dispatch(actions.deleteSetInit())

    if (isNil(setValue)) {
      // gather all values for this set and it's descendants
      const { values } = getDescendants(getState().interview.values, getState().interview.sets, set)

      return Promise.all(values.map((value) => ValueApi.deleteValue(projectId, value)))
        .then(() => {
          dispatch(updateProgress())
          dispatch(deleteSetSuccess(set))
        })
        .catch((errors) => dispatch(actions.deleteSetError(errors)))
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
        .catch((errors) => dispatch(actions.deleteSetError(errors)))
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
    dispatch(actions.copySetInit())

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
      .catch((errors) => dispatch(actions.copySetError(errors)))
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
