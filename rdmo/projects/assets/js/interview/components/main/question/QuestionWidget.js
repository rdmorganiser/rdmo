import React from 'react'
import PropTypes from 'prop-types'

import CheckboxWidget from '../widget/CheckboxWidget'
import DateWidget from '../widget/DateWidget'
import FileWidget from '../widget/FileWidget'
import RadioWidget from '../widget/RadioWidget'
import RangeWidget from '../widget/RangeWidget'
import SelectWidget from '../widget/SelectWidget'
import TextWidget from '../widget/TextWidget'
import TextareaWidget from '../widget/TextareaWidget'
import YesNoWidget from '../widget/YesNoWidget'

const QuestionWidget = (props) => {
  switch (props.question.widget_type) {
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
    case 'autocomplete':
      return <SelectWidget {...props} />
    case 'freeautocomplete':
      return <SelectWidget {...props} creatable={true} />
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
