import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionSetHelp = ({ questionset }) => {
  const classnames = classNames({
    'help-text': true
  })

  return !isEmpty(questionset.help) && (
    <Html className={classnames} html={questionset.help} />
  )
}

QuestionSetHelp.propTypes = {
  questionset: PropTypes.object.isRequired
}

export default QuestionSetHelp
