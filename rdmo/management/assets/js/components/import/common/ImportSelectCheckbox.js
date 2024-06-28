import React from 'react'
import PropTypes from 'prop-types'
import { CodeLink } from '../../common/Links'
import { codeClass, verboseNames } from '../../../constants/elements'

const ImportSelectCheckbox = ({ element, toggleImport, updateShowField }) => (
  <div className="checkbox">
    <label className="mr-5">
      <input type="checkbox" checked={element.import} onChange={toggleImport} />
      <strong>{verboseNames[element.model]}{' '}</strong>
    </label>
    <CodeLink className={codeClass[element.model]} uri={element.uri} onClick={updateShowField} />
   {
      (element.changed && element.updated) &&
        <span className="label label-info ml-5" onClick={updateShowField}>
          {gettext('changed')}</span>
    }
    {
      element.created &&
        <span className="label label-success ml-5" onClick={updateShowField}>
          {gettext('created')}</span>
    }
  </div>
)

ImportSelectCheckbox.propTypes = {
  element: PropTypes.object.isRequired,
  toggleImport: PropTypes.func.isRequired,
  updateShowField: PropTypes.func.isRequired
}

export default ImportSelectCheckbox
