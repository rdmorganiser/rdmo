import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

const QuestionSetHelp = ({ questionset }) => {
  const classnames = classNames({
    'help-text': true
  })

  return !isEmpty(questionset.help) && (
    <div className={classnames} dangerouslySetInnerHTML={{ __html: questionset.help }}></div>
  )
}

QuestionSetHelp.propTypes = {
  questionset: PropTypes.object.isRequired
}

export default QuestionSetHelp
