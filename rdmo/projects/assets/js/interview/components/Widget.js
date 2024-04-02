import React from 'react'
import PropTypes from 'prop-types'

import Autocomplete from './widgets/Autocomplete'
import Checkbox from './widgets/Checkbox'
import Date from './widgets/Date'
import File from './widgets/File'
import Radio from './widgets/Radio'
import Range from './widgets/Range'
import Select from './widgets/Select'
import Text from './widgets/Text'
import Textarea from './widgets/Textarea'
import YesNo from './widgets/YesNo'

const Widget = ({ question }) => {
  switch (question.widget_type) {
    case 'autocomplete':
      return <Autocomplete question={question} />
    case 'checkbox':
      return <Checkbox question={question} />
    case 'date':
      return <Date question={question} />
    case 'file':
      return <File question={question} />
    case 'radio':
      return <Radio question={question} />
    case 'range':
      return <Range question={question} />
    case 'select':
      return <Select question={question} />
    case 'text':
      return <Text question={question} />
    case 'textarea':
      return <Textarea question={question} />
    case 'yesno':
      return <YesNo question={question} />
  }
}

Widget.propTypes = {
  question: PropTypes.object.isRequired
}

export default Widget
