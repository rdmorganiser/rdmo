import React from 'react'

const QuestionOptional = () => {
  return (
    <div className="badge badge-optional" title={gettext('This is an optional question.')}>
      {gettext('Optional')}
    </div>
  )
}

export default QuestionOptional
