import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import isString from 'lodash/isString'
import isUndefined from 'lodash/isUndefined'
import truncate from 'lodash/truncate'
import { codeClass } from '../../../constants/elements'
import {isNull} from 'lodash'

const serializeValue = (value) => {
  if (value === null) return ''
  if (value === true) return 'true'
  if (value === false) return 'false'
  if (Array.isArray(value)) return value
  if (isString(value)) return value
  if (typeof value === 'number') return value.toString()
  return value
}


const FieldRowValue = ({ value }) => {
  const serializedValue = serializeValue(value)
  return  (
    <div className="col-sm-12">
      {Array.isArray(value) && (
        <ul className="list-unstyled mb-0">
          {value.map((el) => (
            <li key={uniqueId()}>
              <code className={codeClass[el.type]}>{el.uri}</code>
            </li>
          ))}
        </ul>
      )}
      {!isNull(value) && !isUndefined(value.uri) && <code className={codeClass[value.type]}>{value.uri}</code>}
      {isString(serializedValue) && <span>{truncate(value, { length: 512 })}</span>}
    </div>
  )
}

FieldRowValue.propTypes = {
  value: PropTypes.any.isRequired,
}

export default FieldRowValue
