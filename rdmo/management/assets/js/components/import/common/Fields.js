import React from 'react'
import PropTypes from 'prop-types'
import isNil from 'lodash/isNil'
import uniqueId from 'lodash/uniqueId'
import FieldRow from './FieldRow'

const excludeKeys = [
  'import',
  'key',
  'model',
  'show',
  'type',
  'uri',
  'uri_path',
  'uri_prefix',
  'valid',
  'created',
  'updated',
  'errors',
  'warnings',
  'updated_and_changed',
  'changed',
  'changedFields',
  'locked'
]

const Fields = ({ element }) => (
  <div className="mt-10">
    {Object.entries(element)
      .sort()
      .map(([key, value]) => {
        if ((!isNil(value) || key in element.updated_and_changed) && !excludeKeys.includes(key)) {
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
