import React from 'react'
import PropTypes from 'prop-types'

import AutocompleteWidget from './widgets/AutocompleteWidget'
import CheckboxWidget from './widgets/CheckboxWidget'
import DateWidget from './widgets/DateWidget'
import FileWidget from './widgets/FileWidget'
import RadioWidget from './widgets/RadioWidget'
import RangeWidget from './widgets/RangeWidget'
import SelectWidget from './widgets/SelectWidget'
import TextWidget from './widgets/TextWidget'
import TextareaWidget from './widgets/TextareaWidget'
import YesNoWidget from './widgets/YesNoWidget'

const QuestionWidget = (props) => {
  switch (props.question.widget_type) {
    case 'autocomplete':
      return <AutocompleteWidget {...props} />
    case 'checkbox':
      return <CheckboxWidget {...props} />
    case 'date':
      return <DateWidget {...props} />
    case 'file':
      return <FileWidget {...props} />
    case 'radio':
      return <RadioWidget {...props} />
    case 'range':
      return <RangeWidget {...props} />
    case 'select':
      return <SelectWidget {...props} />
    case 'text':
      return <TextWidget {...props} />
    case 'textarea':
      return <TextareaWidget {...props} />
    case 'yesno':
      return <YesNoWidget {...props} />
    default:
      return null
  }
}

QuestionWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default QuestionWidget
