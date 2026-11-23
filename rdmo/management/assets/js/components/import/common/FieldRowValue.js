import React from 'react'
import PropTypes from 'prop-types'
import isPlainObject from 'lodash/isPlainObject'
import isString from 'lodash/isString'
import isUndefined from 'lodash/isUndefined'
import truncate from 'lodash/truncate'
import uniqueId from 'lodash/uniqueId'

import { codeClass } from '../../../constants/elements'


const FieldRowValue = ({ value }) => {
  return  (
    <div className="mt-1">
      {
        Array.isArray(value) && (
          <ul className="list-unstyled">
            {
              value.map((el) => (
                <li key={uniqueId()}>
                  <code className={codeClass[el.model]}>{el.uri}</code>
                </li>
              ))
            }
          </ul>
        )
      }
      {
        isPlainObject(value) && !isUndefined(value.uri) &&
        <code className={codeClass[value.model || 'domain.attribute']}>{value.uri}</code>
      }
      {
        isString(value) &&
        <span>{truncate(value, { length: 512 })}</span>
      }
    </div>
  )
}

FieldRowValue.propTypes = {
  value: PropTypes.any.isRequired,
}

export default FieldRowValue
