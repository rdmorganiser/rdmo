import React from 'react'
import PropTypes from 'prop-types'

import FieldRowValue from './FieldRowValue'
import FieldRowDiffs from './FieldRowDiffs'

const FieldRow = ({ element, keyName, value }) => {
  const fieldDiffData = element.updated_and_changed?.[keyName]
  const showDiff = element.updated && element.changed && fieldDiffData?.changed

  return (
    <div className="import-card card mb-2">
      <div className="card-body">
        <div className="row">
          <div className="col-sm-3 mb-5 mt-5">
            <code className="code-import">{keyName}</code>
          </div>
        </div>
        <div className="row">
          {
            showDiff ? (
              <FieldRowDiffs element={element} field={keyName} />
            ) : (
              <FieldRowValue value={value} />
            )
          }
        </div>
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
