import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import isString from 'lodash/isString'
import isUndefined from 'lodash/isUndefined'
import truncate from 'lodash/truncate'
import {codeClass} from '../../../constants/elements'
import {isNull} from 'lodash'


const FieldRowValue = ({ value }) => {

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
      {isString(value) && <span>{truncate(value, { length: 512 })}</span>}
    </div>
  )
}

FieldRowValue.propTypes = {
  value: PropTypes.any.isRequired,
}

export default FieldRowValue
