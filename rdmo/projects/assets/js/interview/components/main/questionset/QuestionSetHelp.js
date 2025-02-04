import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionSetHelp = ({ questionset }) => {
  return !isEmpty(questionset.help) && (
    <div className="interview-questionset-help">
      <Html html={questionset.help} />
    </div>
  )
}

QuestionSetHelp.propTypes = {
  questionset: PropTypes.object.isRequired
}

export default QuestionSetHelp
