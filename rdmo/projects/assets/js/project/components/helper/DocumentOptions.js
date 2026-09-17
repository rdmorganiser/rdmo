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
    } else if(field == 'hideAnswers'){
      const current = isTruthy(get(config, 'document.hideAnswers', false))
      dispatch(configActions.updateConfig('document.hideAnswers', !current))
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
      <li>
        <label className="dropdown-item">
          <input
            type="checkbox"
            checked={isTruthy(get(config, 'document.hideAnswers'))}
            className="form-check-input"
            onChange={(event) => handleClick(event, 'hideAnswers')}/>
        &nbsp; {gettext('Hide answers')}
        </label>
      </li>
    </div>
  )
}

DocumentOptions.propTypes = {
  onChanged: PropTypes.func
}

export default DocumentOptions
