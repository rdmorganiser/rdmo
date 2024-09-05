import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import FieldRowValue from './FieldRowValue'
import FieldRowDiffs from './FieldRowDiffs'

const FieldRow = ({ element, keyName, value }) => {

  return (
    <div>
      <div className="row" key={uniqueId()}>
        <div className="col-sm-3 mb-5 mt-5">
          <code className="code-import">{keyName}</code>
        </div>
      </div>
      <div className="row" key={uniqueId()}>
        <FieldRowValue value={value} />
        {element.updated && element.changed && keyName in element.updated_and_changed && (
          <FieldRowDiffs element={element} field={keyName} />
        )}
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
