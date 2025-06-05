import { isEmpty, isNil, toNumber, toString, last, sortBy } from 'lodash'

import SetFactory from '../factories/SetFactory'

export const getParentSet = (set) => {
  const split = set.set_prefix.split('|')

  return {
    set_prefix: (split.length > 1) ? split.slice(0, -1).join('|') : '',
    set_index: toNumber(last(split)),
    element: set.element.parent
  }
}

export const getChildPrefix = (set) => {
  return isEmpty(set.set_prefix) ? toString(set.set_index) : `${set.set_prefix}|${set.set_index}`
}

export const getSetPrefixLength = (value) => (
  isEmpty(value.set_prefix) ? 0 : value.set_prefix.split('|').length
)

export const generateSetIndex = (sets, set) => {
  const lastSet = last(sortBy(sets.filter(s => (
    (s.set_prefix == set.set_prefix) &&
    (s.element == set.element)
  )), ['set_index']))

  return lastSet ? lastSet.set_index + 1 : 0
}

export const getDescendants = (values, sets, set) => {
  // get all descendant sets for this set and this element and all its descendant questionsets
  const descendantSets = sets.filter((s) => (
    (
      (
        (s.set_prefix === set.set_prefix) &&
        (s.set_index === set.set_index)
      ) || (
        (s.set_prefix.startsWith(getChildPrefix(set)))
      )
    ) && [set.element, ...set.element.questionsets].includes(s.element)
  ))

  // get all values for this set, including it's descendant sets
  const descendantValues = values.reduce((descendantValues, value) => {
    // append values for which a descendant set with matching set_prefix and set_index exists,
    // whose element also has a question with the same attribute as the the value
    return descendantSets.find(set => (
      (set.set_prefix == value.set_prefix) &&
      (set.set_index == value.set_index) &&
      (set.element.attributes.includes(value.attribute))
    )) ? [...descendantValues, value] : descendantValues
  }, [])

  return { sets: descendantSets, values: descendantValues }
}

export const findSetsForElement = (values, element) => {
  return values
    .filter((value) => (
      (element.attributes.includes(value.attribute)) &&
      (getSetPrefixLength(value) == element.level)
    ))
    .reduce((sets, value) => {
      if (sets.find((set) => (
        (set.set_prefix === value.set_prefix) &&
        (set.set_index === value.set_index)
      ))) {
        return sets
      } else {
        return [...sets, SetFactory.create({
          set_prefix: value.set_prefix,
          set_index: value.set_index,
          element
        })]
      }
    }, [])
}

export const gatherSets = (values, element) => {
  // get the values for the questions of this page/questionset
  const currentQuestionsets = element.elements.filter((e) => (e.model === 'questions.questionset'))
  const currentSets = findSetsForElement(values, element)

  // recursively reduce over child questionsets
  const childSets = currentQuestionsets.reduce((sets, questionset) => (
    [...sets, ...gatherSets(values, questionset)]
  ), [])

  // create a list of all currentSets and childSets
  let sets = [...currentSets, ...childSets]

  // ensure that every child set has a parent
  childSets.forEach((set) => {
    createSetIfNotExisting(sets, getParentSet(set))
  })

  // return the sorted sets
  return sortBy(sets, ['element.id', 'set_prefix', 'set_index'])
}

export const initSets = (sets, element, set_prefix) => {
  if (isNil(set_prefix)) {
    set_prefix = ''
  }

  // if this element is not a collection, create at least one valueset
  if (!element.is_collection) {
    createSetIfNotExisting(sets, {
      set_prefix,
      set_index: 0,
      element
    })
  }

  // get the sets of the element
  const currentSets = sets.filter((set) => (
    (set.set_prefix === set_prefix) &&
    (set.element === element)
  ))

  // get the (direct) questionsets of the element
  const currentQuestionsets = element.elements.filter((e) => (e.model === 'questions.questionset'))

  // recursively loop over the current sets the current questionsets
  currentSets.forEach((set) => {
    currentQuestionsets.forEach((questionset) => {
        initSets(sets, questionset, getChildPrefix(set))
      })
  })
}

export const createSetIfNotExisting = (sets, set) => {
    if (!sets.find((s) => ((
      (s.set_prefix === set.set_prefix) &&
      (s.set_index === set.set_index) &&
      (s.element === set.element)
    )))) {
      sets.push(SetFactory.create(set))
    }
}

export const copyResolvedConditions = (originalSets, sets) => {
  sets.forEach((set) => {
    const originalSet = originalSets.find(originalSet => (
      (originalSet.set_prefix == set.set_prefix) &&
      (originalSet.set_index == set.set_index) &&
      (originalSet.element === set.element)
    ))

    if (!isNil(originalSet)) {
      ['questionsets', 'questions', 'optionsets'].forEach(elementType => {
        if (!isNil(originalSet[elementType])) {
          set[elementType] = originalSet[elementType]
        }
      })
    }
  })
}
