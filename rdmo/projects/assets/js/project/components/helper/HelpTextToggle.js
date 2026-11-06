import React from 'react'
import PropTypes from 'prop-types'

import { Link } from 'rdmo/core/assets/js/components'
import { useConfig } from 'rdmo/core/assets/js/hooks'

const HelpTextToggle = ({ onChanged }) => {
  const [includeHelp, setIncludeHelp] = useConfig('document.includeHelp', false)

  const handleClick = () => {
    setIncludeHelp(!includeHelp)

    if(onChanged){
      onChanged()
    }
  }

  return (
    <Link onClick={handleClick}>
      {includeHelp && gettext('Hide help texts') || gettext('Show help texts')}
    </Link>
  )
}

HelpTextToggle.propTypes = {
  onChanged: PropTypes.func
}

export default HelpTextToggle
