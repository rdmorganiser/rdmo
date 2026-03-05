import React from 'react'
import PropTypes from 'prop-types'

import FieldRowValue from './FieldRowValue'
import FieldRowDiffs from './FieldRowDiffs'

const FieldRow = ({ element, keyName, value }) => {

  return (
    <div className="import-card card mb-2">
      <div className="card-body">
        <small>{keyName}</small>

        <FieldRowValue value={value} />

        {
          element.updated && element.changed && keyName in element.updated_and_changed && (
            <FieldRowDiffs element={element} field={keyName} />
          )
        }
      </div>
    </div>
  )
}

FieldRow.propTypes = {
  element: PropTypes.object.isRequired,
  keyName: PropTypes.string.isRequired,
  value: PropTypes.any.isRequired,
}

export default FieldRow
