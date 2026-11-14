import React from 'react'
import PropTypes from 'prop-types'

import { LinkButton } from 'rdmo/core/assets/js/components'
import { useConfigToggle } from 'rdmo/core/assets/js/hooks'

const HelpTextToggle = ({ onChanged }) => {
  const [includeHelp, toggleIncludeHelp] = useConfigToggle('document.includeHelp')

  const handleClick = () => {
    toggleIncludeHelp()

    if(onChanged){
      onChanged()
    }
  }

  return (
    <LinkButton onClick={handleClick}>
      {includeHelp && gettext('Hide help texts') || gettext('Show help texts')}
    </LinkButton>
  )
}

HelpTextToggle.propTypes = {
  onChanged: PropTypes.func
}

export default HelpTextToggle
