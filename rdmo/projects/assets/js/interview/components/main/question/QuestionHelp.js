import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

const QuestionHelp = ({ question }) => {
  const classnames = classNames({
    'help-text': true,
    'text-muted': question.is_optional
  })

  return !isEmpty(question.help) && (
    <div className={classnames} dangerouslySetInnerHTML={{ __html: question.help }}></div>
  )
}

QuestionHelp.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionHelp
