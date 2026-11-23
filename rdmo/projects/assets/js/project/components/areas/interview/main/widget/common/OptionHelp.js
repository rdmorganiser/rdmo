import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

const OptionHelp = ({ className, option }) => {
  return !isEmpty(option.help) && (
    <span className={className}>
      <Html className="option-help text-muted" html={option.help} />
    </span>
  )
}

OptionHelp.propTypes = {
  className: PropTypes.string,
  option: PropTypes.object.isRequired
}

export default OptionHelp
