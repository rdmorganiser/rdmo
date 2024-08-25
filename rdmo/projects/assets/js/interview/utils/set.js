import { isEmpty, isNil, toNumber, toString, last, sortBy } from 'lodash'

import SetFactory from '../factories/SetFactory'

const getParentSet = (set) => {
  const split = set.set_prefix.split('|')

  return {
    set_prefix: (split.length > 1) ? split.slice(0, -1).join('|') : '',
    set_index: toNumber(last(split))
  }
}

const getChildPrefix = (set) => {
  return isEmpty(set.set_prefix) ? toString(set.set_index) : `${set.set_prefix}|${set.set_index}`
}

const getDescendants = (items, set) => {
  return items.filter((item) => (
    (
      (item.set_prefix === set.set_prefix) &&
      (item.set_index === set.set_index)
    ) || (
      (item.set_prefix.startsWith(getChildPrefix(set)))
    )
  ))
}

const gatherSets = (values) => {
  const sets = values.reduce((sets, value) => {
    if (sets.find((set) => (
      (set.set_prefix === value.set_prefix) &&
      (set.set_index === value.set_index)
    ))) {
      return sets
    } else {
      return [...sets, SetFactory.create({
        set_prefix: value.set_prefix,
        set_index: value.set_index
      })]
    }
  }, [])

  return sortBy(sets, ['set_prefix', 'set_index'])
}

const initSets = (sets, element, setPrefix) => {
  if (isNil(setPrefix)) {
    setPrefix = ''
  }

  // for non collection questionsets create at least one valueset (for this set_prefix)
  if (!element.is_collection) {
    if (!sets.find((set) => (
      (set.set_prefix === setPrefix) && (
      (set.set_index === 0)
    )))) {
      sets.push(SetFactory.create({
        set_prefix: setPrefix
      }))
    }
  }

  // create sets for which contain other sets but no (direct) values
  sets.filter((set) => ((set.set_prefix !== setPrefix) && set.set_prefix.startsWith(setPrefix))).forEach((set) => {
    const parentSet = getParentSet(set)

    if (!sets.find((set) => ((
      (set.set_prefix === parentSet.set_prefix) &&
      (set.set_index === parentSet.set_index)
    )))) {
      sets.push(SetFactory.create(parentSet))
    }
  })

  // recursively loop over child questionsets and sets
  element.elements.filter((e) => (e.model === 'questions.questionset')).forEach((questionset) => {
    sets.filter((set) => set.set_prefix === setPrefix).forEach((set) => {
      initSets(sets, questionset, getChildPrefix(set))
    })
  })
}

export { getParentSet, getChildPrefix, getDescendants, gatherSets, initSets }
