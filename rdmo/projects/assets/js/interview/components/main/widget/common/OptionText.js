import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const OptionText = ({ className, option }) => {
  return (
    <span className={className}>
      <Html className="option-text" html={option.text} />
    </span>
  )
}

OptionText.propTypes = {
  className: PropTypes.string,
  option: PropTypes.object.isRequired
}

export default OptionText
