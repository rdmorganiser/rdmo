import React from 'react'
import PropTypes from 'prop-types'
import isString from 'lodash/isString'

import Field from './Field'

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


export const serializeValue = (value) => {
  if (value === null) return ''
  if (value === true) return 'true'
  if (value === false) return 'false'
  if (Array.isArray(value)) return value
  if (isString(value)) return value
  if (typeof value === 'number') return value.toString()
  return value
}

const Fields = ({ element }) => {

  return (
    <div>
      {Object.entries(element)
        .sort()
        .map(([key, value]) => {
          if (!excludeKeys.includes(key)) {
            const serializedValue = serializeValue(value)
            if (serializedValue !== '' || (element.changedFields?.includes(key))) {
              return <Field key={key} element={element} keyName={key} value={serializedValue} />
            }
          }
          return null
        })}
    </div>
  )
}

Fields.propTypes = {
  element: PropTypes.object.isRequired,
}

export default Fields
