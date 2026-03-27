import React from 'react'
import PropTypes from 'prop-types'
import { uniqueId } from 'lodash'

import { elementModules, verboseNames } from '../../../constants/elements'

import { CodeLink } from '../../common/Links'

const ImportSelectCheckbox = ({ element, toggleImport, updateShowField }) => {
  const id = uniqueId('import-checkbox-')
  const changedLabelText = gettext('Changed')
  const createdLabelText = gettext('New')

  return (
    <>
      <div className="form-check">
        <input type="checkbox" htmlFor={id} className="form-check-input" checked={element.import}
          onChange={toggleImport} />
        <label className="form-check-label" htmlFor={id}>{verboseNames[element.model]}</label>
      </div>

      <CodeLink className="flex-grow-1" type={elementModules[element.model]} uri={element.uri} onClick={updateShowField} />

      {
        (element.changed && element.updated) && (
          <span className="badge text-bg-info">
            {changedLabelText}
          </span>
        )
      }

      {
        element.created && (
          <span className="badge text-bg-success">
            {createdLabelText}
          </span>
        )
      }
    </>
  )
}

ImportSelectCheckbox.propTypes = {
  element: PropTypes.object.isRequired,
  toggleImport: PropTypes.func.isRequired,
  updateShowField: PropTypes.func.isRequired
}

export default ImportSelectCheckbox
