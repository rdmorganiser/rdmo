import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

const OptionHelp = ({ className, option }) => {
  return !isEmpty(option.help) && (
    <span className={className}>
      <span className="option-help text-muted" dangerouslySetInnerHTML={{ __html: option.help }}></span>
    </span>
  )
}

OptionHelp.propTypes = {
  className: PropTypes.string,
  option: PropTypes.object.isRequired
}

export default OptionHelp
