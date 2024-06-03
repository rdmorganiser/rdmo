import React from 'react'
import PropTypes from 'prop-types'
import isNil from 'lodash/isNil'
import uniqueId from 'lodash/uniqueId'
import FieldRow from './FieldRow'

const excludeKeys = [
  'created',
  'errors',
  'import',
  'key',
  'model',
  'show',
  'type',
  'updated',
  'uri',
  'uri_path',
  'uri_prefix',
  'valid',
  'warnings',
  'updated_and_changed',
  'changed',
  'changedFields',
]

const Fields = ({ element }) => (
  <div className="mt-10">
    {Object.entries(element)
      .sort()
      .map(([key, value]) => {
        if (!isNil(value) && !excludeKeys.includes(key)) {
          return <FieldRow key={uniqueId()} element={element} keyName={key} value={value} />
        }
        return null
      })}
  </div>
)

Fields.propTypes = {
  element: PropTypes.object.isRequired,
}

export default Fields
