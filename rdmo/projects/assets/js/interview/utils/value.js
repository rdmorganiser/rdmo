import { isNil } from 'lodash'

import ValueFactory from '../factories/ValueFactory'

import { getChildPrefix } from './set'

const initValues = (sets, values, element, setPrefix) => {
  if (isNil(setPrefix)) {
    setPrefix = ''
  }

  sets.filter((set) => set.set_prefix === setPrefix).forEach((set) => {
    element.elements.filter((e) => (e.model === 'questions.question')).forEach((question) => {
      if (isNil(values.find((value) => (
        (value.attribute === question.attribute) &&
        (value.set_prefix == set.set_prefix) &&
        (value.set_index == set.set_index)
      )))) {
        const value = ValueFactory.create({
          attribute: question.attribute,
          set_prefix: set.set_prefix,
          set_index: set.set_index
        })

        if (question.widget_class === 'range') {
          initRange(value)
        }

        values.push(value)
      }
    })

    element.elements.filter((e) => (e.model === 'questions.questionset')).forEach((questionset) => {
      initValues(sets, values, questionset, getChildPrefix(set))
    })
  })
}

const initRange = (question, value) => {
  value.text = isNil(question.minimum) ? 0 : question.minimum
}

export { initValues, initRange }
