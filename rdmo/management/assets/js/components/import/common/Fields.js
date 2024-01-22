import React from 'react'
import PropTypes from 'prop-types'
import isNil from 'lodash/isNil'
import isString from 'lodash/isString'
import isUndefined from 'lodash/isUndefined'
import truncate from 'lodash/truncate'
import uniqueId from 'lodash/uniqueId'
import isEmpty from 'lodash/isEmpty'


import { codeClass } from '../../../constants/elements'
import FieldsDiffs from './FieldsDiffs'

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
  'original',
  'updated_and_changed',
]

const Fields = ({ element }) => {
  return (
    <div className="mt-10">
      {
        Object.entries(element).sort().map(([key, value]) => {
          if (!isNil(value) && !excludeKeys.includes(key)) {
            return (
              <div key={uniqueId()} className="row">
                <div className="col-sm-3 text-right">
                  <code className="code-import">{key}</code>
                </div>
                <div className="col-sm-9">
                  {
                    Array.isArray(value) && <ul className="list-unstyled mb-0">
                      { value.map(el => <li key={uniqueId()}>
                        <code className={codeClass[el.type]}>{el.uri}</code>
                      </li>) }
                    </ul>
                  }
                  {
                    !isUndefined(value.uri) && <code className={codeClass[value.type]}>{value.uri}</code>
                  }
                  {
                    isString(value) && <span>{truncate(value, {length: 512})}</span>
                  }
                </div>
                {
                  isEmpty(element.errors) && !isEmpty(element.updated_and_changed) && element.updated &&
                  key in element.updated_and_changed && <FieldsDiffs element={element} field={key}/>
                  }
              </div>
            )
          }
        })
      }
    </div>
  )
}

Fields.propTypes = {
  element: PropTypes.object.isRequired
}

export default Fields
