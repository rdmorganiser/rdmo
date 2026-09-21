import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import { get } from 'lodash'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

const DocumentOptions = ({ onChanged }) => {
  const dispatch = useDispatch()
  const config = useSelector((state) => state.config)

  const toggleDocumentOption = (field) => {
    if(field == 'includeHelp'){
      const current = isTruthy(get(config, 'document.includeHelp', false))
      dispatch(configActions.updateConfig('document.includeHelp', !current))
    }
  }

  const handleClick = (event, field) => {
    event.stopPropagation()
    toggleDocumentOption(field)
    if(onChanged){
      onChanged(field)
    }
  }

  return (
    <div className="form-switch" onClick={(event) => event.stopPropagation()}>
      <li>
        <label className="dropdown-item">
          <input
            type="checkbox"
            checked={isTruthy(get(config, 'document.includeHelp'))}
            className="form-check-input"
            onChange={(event) => handleClick(event, 'includeHelp')}/>
        &nbsp; {gettext('Include help')}
        </label>
      </li>
    </div>
  )
}

DocumentOptions.propTypes = {
  onChanged: PropTypes.func
}

export default DocumentOptions
