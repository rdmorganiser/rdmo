import React from 'react'
import PropTypes from 'prop-types'

const QuestionDefault = ({ isDefault }) => {
  return isDefault && (
    <div className="badge badge-default" title={gettext('This is a default answer that can be customized.')}>
      {gettext('Default')}
    </div>
  )
}

QuestionDefault.propTypes = {
  isDefault: PropTypes.bool.isRequired
}

export default QuestionDefault
