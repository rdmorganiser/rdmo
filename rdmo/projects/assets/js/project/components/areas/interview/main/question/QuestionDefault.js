import React from 'react'
import PropTypes from 'prop-types'

import { isDefaultValue } from '../../../utils/value'

const QuestionDefault = ({ question, value }) => {
  return isDefaultValue(question, value) && (
    <div className="badge badge-default" title={gettext('This is a default answer that can be customized.')}>
      {gettext('Default')}
    </div>
  )
}

QuestionDefault.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired
}

export default QuestionDefault
