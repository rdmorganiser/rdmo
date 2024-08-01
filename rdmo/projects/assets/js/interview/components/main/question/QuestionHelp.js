import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionHelp = ({ question }) => {
  const classnames = classNames({
    'help-text': true,
    'text-muted': question.is_optional
  })

  return <Html className={classnames} html={question.help} />
}

QuestionHelp.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionHelp
