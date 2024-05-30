import React from 'react'
import PropTypes from 'prop-types'

const OptionText = ({ className, option }) => {
  return (
    <span className={className}>
      <span className="option-text" dangerouslySetInnerHTML={{ __html: option.text }}></span>
    </span>
  )
}

OptionText.propTypes = {
  className: PropTypes.string,
  option: PropTypes.object.isRequired
}

export default OptionText
