import { isNil, toString } from 'lodash'

import ValueFactory from '../factories/ValueFactory'

import { getChildPrefix } from './set'

const isDefaultValue = (question, value) => {
  if (isNil(value.id)) {
    if (question.default_text) {
      return question.default_text == value.text
    } else if (question.default_option) {
      return toString(question.default_option) == value.option
    } else if (question.default_external_id) {
      return question.default_external_id == value.external_id
    }
  } else {
    return false
  }
}

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
          set_index: set.set_index,
          text: question.default_text,
          option: question.default_option,
          external_id: question.default_external_id
        })

        if (question.widget_class === 'range') {
          initRange(question, value)
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
  if (isNil(value.text)) {
    value.text = isNil(question.minimum) ? 0 : question.minimum
  }
}

export { isDefaultValue, initValues, initRange }
