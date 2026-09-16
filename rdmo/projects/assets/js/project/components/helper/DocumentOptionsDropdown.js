import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import { get } from 'lodash'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

const SnapshotsDropdown = ({ onToggleOption }) => {
  const config = useSelector((state) => state.config)

  const handleClick = (event, field) => {
    event.stopPropagation()

    onToggleOption(field)
  }

  return (
    <div className="dropdown dropdown-menu-end">
      <button
        type="button"
        className="link text-nowrap"
        data-bs-toggle="dropdown"
        data-bs-popper-config='{"strategy":"fixed"}'
        aria-expanded="false"
        onClick={(event) => event.stopPropagation()}
        title={gettext('Document Options')}
      >
        <span>{gettext('Document Options')}</span>
        <i className="bi bi-caret-down-fill ms-1" />
      </button>

      <ul
        className="dropdown-menu" onClick={(event) => event.stopPropagation()}
      >
        <form className="form-switch">
          <li>
            <label className="dropdown-item">
              <input
                type="checkbox"
                checked={isTruthy(get(config, 'document.includeHelp'))}
                className="form-check-input"
                onChange={(event) => handleClick(event, 'includeHelp')}/>
            &nbsp; {gettext('include help')}
            </label>
          </li>
          <li>
            <label className="dropdown-item">
              <input
                type="checkbox"
                checked={isTruthy(get(config, 'document.hideAnswers'))}
                className="form-check-input"
                onChange={(event) => handleClick(event, 'hideAnswers')}/>
            &nbsp; {gettext('hide answers')}
            </label>
          </li>
        </form>
      </ul>
    </div>
  )
}

SnapshotsDropdown.propTypes = {
  onToggleOption: PropTypes.func.isRequired
}

export default SnapshotsDropdown
