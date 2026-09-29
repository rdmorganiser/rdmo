import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import { get } from 'lodash'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

const DocumentOptions = ({ areaTag, onChanged }) => {
  const dispatch = useDispatch()
  const config = useSelector((state) => state.config)

  const toggleDocumentOption = (field) => {
    if(field == 'includeHelp'){
      const current = isTruthy(get(config, `document.${areaTag}.includeHelp`, false))
      dispatch(configActions.updateConfig(`document.${areaTag}.includeHelp`, !current))
    }
    else if(field == 'includeAnswers'){
      const current = isTruthy(get(config, `document.${areaTag}.includeAnswers`, false))
      dispatch(configActions.updateConfig(`document.${areaTag}.includeAnswers`, !current))
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
    <>
      <div className="form-switch" onClick={(event) => event.stopPropagation()}>
        <li>
          <label className="dropdown-item">
            <input
              type="checkbox"
              checked={isTruthy(get(config, `document.${areaTag}.includeHelp`))}
              className="form-check-input"
              onChange={(event) => handleClick(event, 'includeHelp')}/>
        &nbsp; {gettext('Include help')}
          </label>
        </li>
      </div>
      {
        areaTag == 'questions' && (
          <div className="form-switch" onClick={(event) => event.stopPropagation()}>
            <li>
              <label className="dropdown-item">
                <input
                  type="checkbox"
                  checked={isTruthy(get(config, `document.${areaTag}.includeAnswers`))}
                  className="form-check-input"
                  onChange={(event) => handleClick(event, 'includeAnswers')}/>
        &nbsp; {gettext('Include answers')}
              </label>
            </li>
          </div>
        )
      }
    </>
  )
}

DocumentOptions.propTypes = {
  areaTag: PropTypes.string.isRequired,
  onChanged: PropTypes.func,
}

export default DocumentOptions
