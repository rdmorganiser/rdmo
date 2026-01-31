import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { get, isEmpty, isNil, uniqueId } from 'lodash'

import { getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const Radio = ({ element, field, options, onChange }) => {
  const { meta } = useSelector((state) => state.config)

  const label = getLabel(element, field, meta),
        help = getHelp(element, field, meta),
        errors = get(element, ['errors', field])

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className="mb-3">
      <label className="control-label">{label}</label>

      <div className="d-flex align-items-center gap-5">
      {
        options.map((option, index) => {
          const radioId = uniqueId('radio-')

          return (
            <div key={index} className="form-check">
              <input type="radio" id={radioId} disabled={element.read_only}
                     className={classNames('form-check-input', {'is-invalid': !isEmpty(errors)})}
                     checked={value === option.id} value={option.id}
                     onChange={event => onChange(field, event.target.value)} />
              <label className="form-check-label" htmlFor={radioId}>{option.text}</label>
            </div>
          )
        })
      }
      </div>

      <ErrorList errors={errors} />
      <HelpText help={help} />
    </div>
  )
}

Radio.propTypes = {
  className: PropTypes.array,
  element: PropTypes.object,
  field: PropTypes.string,
  options: PropTypes.array,
  onChange: PropTypes.func
}

export default Radio
