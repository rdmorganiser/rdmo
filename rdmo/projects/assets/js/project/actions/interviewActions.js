import { first, isEmpty, isNil, omit } from 'lodash'

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
  compareValueId, compareValues, gatherDefaultValues, initValues, isEmptyValue, sortValues
} from '../utils/value'

import PageApi from '../api/PageApi'
import ProjectApi from '../api/ProjectApi'
import ValueApi from '../api/ValueApi'
import SetFactory from '../factories/SetFactory'
import ValueFactory from '../factories/ValueFactory'

import { fetchNavigation, fetchProgress, updateProgress } from './projectActions'

// returns a dispatch function, which ignores actions if the page was changed in the meantime
const getDispatchOnPage = (dispatch, getState, page) => (action) => (
  getState().interview.page === page ? dispatch(action) : null
)

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

        dispatch(actions.fetchPageSuccess({ page }))

        dispatch(fetchValues(page))
        dispatch(fetchOptionsets(page))

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

export function refreshPage(values = []) {
  return (dispatch, getState) => {
    const page = getState().interview.page
    const sets = getState().interview.sets

    // check if one of the questions for the given values has an optionset with the refresh flag
    const attributes = values.map((value) => value.attribute)
    const refetchValues = page.questions
      .filter((question) => attributes.includes(question.attribute))
      .some((question) => question.optionsets.some((optionset) => optionset.has_refresh))

    dispatch(fetchNavigation())
    dispatch(updateProgress())

    if (refetchValues) {
      // if the refresh flag is set on one of the optionsets, reload all values for the page,
      // resolveConditions will be called in fetchValues. Preserve unsaved values,
      // since they are not included in the response from the backend.
      dispatch(fetchValues(page, true))
    } else {
      dispatch(resolveConditions(page, sets))
    }
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
  const pendingId = `fetchValues/${page.id}`

  return (dispatch, getState) => {
    const dispatchOnPage = getDispatchOnPage(dispatch, getState, page)

    dispatch(addToPending(pendingId))
    dispatchOnPage(clearError('values'))

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

        dispatchOnPage(resolveConditions(page, sets))
        dispatchOnPage(actions.fetchValuesSuccess({ values, sets }))
      })
      .catch((error) => dispatchOnPage(setError('values', error, gettext('Values'))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function resolveConditions(page, sets) {
  const pendingId = 'resolveConditions'

  return (dispatch, getState) => {
    const dispatchOnPage = getDispatchOnPage(dispatch, getState, page)

    dispatch(addToPending(pendingId))
    dispatchOnPage(clearError('conditions'))

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
      .then((results) => dispatchOnPage(actions.resolveConditionsSuccess(results)))
      .catch((error) => dispatchOnPage(setError('conditions', error, gettext('Conditions'))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function storeValue(value, refresh = true) {
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
      const question = page.questions.find((question) => question.attribute === value.attribute)
      const widget_type = question && question.widget_type

      const dispatchOnPage = getDispatchOnPage(dispatch, getState, page)

      const valueText = value.text
      const valueFile = value.file
      const valueSuccess = value.success

      dispatch(addToPending(pendingId))
      dispatchOnPage(actions.storeValueInit(valueId))

      return ValueApi.storeValue(projectId, { ...value, widget_type })
        .then((value) => {
          // if the value was updated while the request was running, store it again
          // (with the id from the response, so that a new value is not created twice)
          const currentValue = getState().interview.values.find((v) => compareValueId(v, valueId))
          const { id, updated } = value
          if (currentValue && currentValue.dirty) {
            const attrs = { id, updated, dirty: false, pending: false }
            dispatchOnPage(actions.updateValue({ value: currentValue, attrs }))
            dispatchOnPage(storeValue({ ...currentValue, ...attrs }))
            return
          }

          if (refresh) {
            dispatch(refreshPage([value]))
          }

          // set the success flag and start the timeout to remove it. the flag is actually
          // the stored timeout, so we can cancel any old timeout before starting the a new
          // one in order to prolong the time the indicator is show with each save
          clearTimeout(valueSuccess)
          value.success = setTimeout(() => {
            dispatchOnPage(updateValue(value, {success: false}, false))
          }, 1000)

          // replace the text with the old text if it was trimmed by the backend
          // (but not if a new text was inserted, e.g. by an optionset provider)
          if (valueText.trim() == value.text) {
            value.text = valueText
          }

          // check if there is a file or if a filename is set (when the file was just erased)
          if (isNil(valueFile) && isNil(value.file_name)) {
            dispatchOnPage(actions.storeValueSuccess({ value, valueId }))
          } else {
            // keep the id from the response in the store, so that the value is not created
            // twice when it is stored again after the file upload failed
            if (currentValue) {
              dispatchOnPage(actions.updateValue({ value: currentValue, attrs: { id, updated } }))
            }

            // upload file after the value is created
            return ValueApi.storeFile(projectId, value, valueFile)
              .then((value) => dispatchOnPage(actions.storeValueSuccess({ value, valueId })))
              .catch((error) => dispatchOnPage(actions.storeValueError({ error: serializeError(error), valueId })))
          }
        })
        .catch((error) => dispatchOnPage(actions.storeValueError({ error: serializeError(error), valueId })))
        .finally(() => dispatch(removeFromPending(pendingId)))
    }
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

    const defaultValues = gatherDefaultValues(page, values).filter((value) => !value.pending)
    if (isEmpty(defaultValues)) {
      return Promise.resolve()
    }

    const dispatchOnPage = getDispatchOnPage(dispatch, getState, page)

    dispatch(addToPending(pendingId))

    return Promise.all(defaultValues.map((value) => {
      const valueId = value.tmp_id

      dispatchOnPage(actions.storeValueInit(valueId))

      return ValueApi.storeValue(projectId, value)
        .then((value) => dispatchOnPage(actions.storeValueSuccess({ value, valueId })))
        .catch((error) => dispatchOnPage(actions.storeValueError({ error: serializeError(error), valueId })))
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
    return (dispatch, getState) => {
      // the value passed from the component might be outdated (e.g. from a debounced input),
      // so the current value is taken from the store and only the attrs are used
      const currentValue = getState().interview.values.find((v) => compareValueId(v, value.id || value.tmp_id)) || value

      const valueToSave = ValueFactory.update({ ...currentValue }, attrs)
      const valueForState = { ...omit(valueToSave, 'file'), dirty: currentValue.pending }

      dispatch(actions.updateValue({ value: currentValue, attrs: valueForState }))
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
    const dispatchOnPage = getDispatchOnPage(dispatch, getState, getState().interview.page)

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

    // update the store right away, siblings which are currently stored are marked as dirty
    copies.forEach(([value, valueId]) => {
      if (isNil(valueId)) {
        dispatchOnPage(actions.createValue(value))
      } else {
        dispatchOnPage(actions.updateValue({ value, attrs: { ...value, dirty: value.pending } }))
      }
    })

    // sort values in the store after the updates
    dispatchOnPage(resortValues())

    return Promise.all(copies.map(([value]) => dispatchOnPage(storeValue(value, false))))
      .then(() => dispatch(refreshPage(copies.map(([value]) => value))))
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
      const dispatchOnPage = getDispatchOnPage(dispatch, getState, getState().interview.page)

      dispatch(addToPending(pendingId))
      dispatchOnPage(actions.deleteValueInit(valueId))

      if (isNil(value.id)) {
        dispatch(removeFromPending(pendingId))
        return dispatchOnPage(actions.deleteValueSuccess(valueId))
      } else {
        return ValueApi.deleteValue(projectId, value)
          .then(() => {
            dispatch(refreshPage([value]))
            dispatchOnPage(actions.deleteValueSuccess(valueId))
          })
          .catch((error) => dispatchOnPage(actions.deleteValueError({ error: serializeError(error), valueId })))
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
    const dispatchOnPage = getDispatchOnPage(dispatch, getState, getState().interview.page)

    // create a new set
    const set = SetFactory.create(attrs)

    // create a value for the text if the page has an attribute
    const value = isNil(attrs.attribute) ? null : ValueFactory.create(attrs)

    // create a callback function to be called immediately or after saving the value,
    // the stored value was already added to the store by storeValueSuccess
    const createSetCallback = () => {
      dispatchOnPage(activateSet(set))

      const state = getState().interview
      const page = state.page
      const sets = [...state.sets, set]
      const values = [...state.values]

      initSets(sets, page)
      initValues(sets, values, page)

      dispatchOnPage(resolveConditions(page, sets))

      return dispatchOnPage(actions.createSet({ values, sets }))
    }

    if (isNil(value)) {
      return createSetCallback()
    } else {
      return dispatchOnPage(storeValue(value)).then(() => {
        const storedValue = getState().interview.values.find((v) => compareValues(v, value))
        if (!isNil(storedValue)) {
          createSetCallback()
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
    const dispatchOnPage = getDispatchOnPage(dispatch, getState, getState().interview.page)

    // gather all values for this set and it's descendants
    const { values } = getDescendants(getState().interview.values, getState().interview.sets, set)

    // do not delete the set while one of its values is stored, since it would be created again,
    // return null, so that the component can check if the set is deleted (e.g. to keep a modal open)
    if (setValue?.pending || values.some((value) => value.pending)) {
      return null
    }

    dispatch(addToPending(pendingId))
    dispatchOnPage(clearError('deleteSet'))

    if (isNil(setValue)) {
      return Promise.all(values.map((value) => ValueApi.deleteValue(projectId, value)))
        .then(() => {
          dispatch(updateProgress())
          dispatchOnPage(deleteSetSuccess(set))
        })
        .catch((error) => dispatchOnPage(setError('deleteSet', error, gettext('Delete set'))))
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
              dispatchOnPage(activateSet(sets[index + 1]))
            } else {
              // If it's the last set, activate the new last set
              dispatchOnPage(activateSet(sets[index - 1]))
            }
          }

          dispatchOnPage(deleteSetSuccess(set))
        })
        .catch((error) => dispatchOnPage(setError('deleteSet', error, gettext('Delete set'))))
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
    const dispatchOnPage = getDispatchOnPage(dispatch, getState, getState().interview.page)

    // do not copy the set while one of its values is stored, since the copy would miss the changes,
    // return null, so that the component can check if the set is copied (e.g. to keep a modal open)
    const { values: descendantValues } = isNil(currentSet) ? { values: [] } : (
      getDescendants(getState().interview.values, getState().interview.sets, currentSet)
    )
    if (copySetValue?.pending || descendantValues.some((value) => value.pending)) {
      return null
    }

    dispatch(addToPending(pendingId))
    dispatchOnPage(clearError('copySet'))

    // create a new set (create) or use the current one (import)
    const set = isNil(attrs.id) ? SetFactory.create(attrs) : currentSet

    // create a value for the text if the page has an attribute (create) or use the current one (import)
    const value = isNil(attrs.attribute) ? null : (
      isNil(attrs.id) ? ValueFactory.create(attrs) : attrs
    )

    // create a callback function to be called immediately or after saving the value
    const copySetCallbackAction = (setValues) => {
      dispatchOnPage(activateSet(set))

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

      dispatchOnPage(resolveConditions(page, sets))
      dispatchOnPage(actions.copySetSuccess({ values, sets }))
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
      .catch((error) => dispatchOnPage(setError('copySet', error, gettext('Copy set'))))
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
