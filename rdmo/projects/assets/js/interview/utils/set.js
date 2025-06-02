import { isEmpty, isNil, toNumber, toString, last, sortBy } from 'lodash'

import SetFactory from '../factories/SetFactory'

export const getParentSet = (set, element) => {
  const split = set.set_prefix.split('|')

  return {
    set_prefix: (split.length > 1) ? split.slice(0, -1).join('|') : '',
    set_index: toNumber(last(split)),
    element
  }
}

export const getChildPrefix = (set) => {
  return isEmpty(set.set_prefix) ? toString(set.set_index) : `${set.set_prefix}|${set.set_index}`
}

export const getDescendants = (values, sets, set) => {
  // get all sets for this element, this includes descendant sets
  const descendantSets = sets.filter((s) => (
    (
      (
        (s.set_prefix === set.set_prefix) &&
        (s.set_index === set.set_index)
      ) || (
        (s.set_prefix.startsWith(getChildPrefix(set)))
      )
    ) && (s.element === set.element)
  ))

  // get all values for this set, including it's descendant sets
  const descendantValues = values.reduce((descendantValues, value) => {
    // append values for which a descendant set with matching set_prefix and set_index exists,
    // whose element also has a question with the same attribute as the the value
    return descendantSets.find(set => (
      (set.set_prefix == value.set_prefix) &&
      (set.set_index == value.set_index) &&
      (set.attributes.includes(value.attribute))
    )) ? [...descendantValues, value] : descendantValues
  }, [])

  return { sets: descendantSets, values: descendantValues }
}

export const gatherSets = (values, element) => {
  const sets = values.reduce((sets, value) => {
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

  return sets
}

export const initSets = (values, element, setPrefix) => {
  if (isNil(setPrefix)) {
    setPrefix = ''
  }

  // gather the (direct) questionsets, questions, and attributes of this element
  const questionsets = element.elements.filter((e) => (e.model === 'questions.questionset'))
  const questions = element.elements.filter((e) => (e.model === 'questions.question'))
  const attributes = [
    ...(isNil(element.attribute) ? [] : [element.attribute]),
    ...questions.map((question) => question.attribute)
  ]

  // get the values for the questions of this page/questionset
  const currentValues = values.filter((value) => attributes.includes(value.attribute))
  const currentSets = gatherSets(currentValues, element)

  // for non collection questionsets create at least one valueset (for this set_prefix)
  if (!element.is_collection) {
    if (!currentSets.find((set) => (
      (set.set_prefix === setPrefix) && (
      (set.set_index === 0)
    )))) {
      currentSets.push(SetFactory.create({
        set_prefix: setPrefix,
        element
      }))
    }
  }

  // recursively reduce over child questionsets, start with current sets
  const childSets = questionsets.reduce((sets, questionset) => (
    [...sets, ...initSets(values, questionset)]
  ), [])

  // create a list of all currentSets, childSets and a copy of childSets, but for this element
  let sets = [
    ...currentSets,
    ...childSets,
    ...childSets.map(set => SetFactory.create({
      ...set,
      element
    }))
  ]

  // ensure that there is a set for the current setPrefix for each child set
  childSets.forEach((set) => {
    const parentSet = getParentSet(set, element)

    if (!sets.find((set) => ((
      (set.set_prefix === parentSet.set_prefix) &&
      (set.set_index === parentSet.set_index)
    )))) {
      sets.push(SetFactory.create(parentSet))
    }
  })

  // return the sorted sets
  return sortBy(sets, ['questionset', 'set_prefix', 'set_index'])
}

export const copyResolvedConditions = (originalSets, sets) => {
  sets.forEach((set) => {
    const originalSet = originalSets.find(originalSet => (
      originalSet.set_prefix == set.set_prefix) && (originalSet.set_index == set.set_index)
    )

    if (!isNil(originalSet)) {
      ['questionsets', 'questions', 'optionsets'].forEach(elementType => {
        if (!isNil(originalSet[elementType])) {
          set[elementType] = originalSet[elementType]
        }
      })
    }
  })
}
