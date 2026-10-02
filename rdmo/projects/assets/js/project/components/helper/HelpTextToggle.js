import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import { get } from 'lodash'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { Link } from 'rdmo/core/assets/js/components'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

const HelpTextToggle = ({ onChanged }) => {
  const dispatch = useDispatch()
  const config = useSelector((state) => state.config)

  const handleClick = () => {
    const current = isTruthy(get(config, 'document.includeHelp', false))
    dispatch(configActions.updateConfig('document.includeHelp', !current))

    if(onChanged){
      onChanged()
    }
  }

  return (
    <Link onClick={handleClick}>
      {isTruthy(get(config, 'document.includeHelp')) && gettext('Remove help text') || gettext('Include help text')}
    </Link>
  )
}

HelpTextToggle.propTypes = {
  onChanged: PropTypes.func
}

export default HelpTextToggle
