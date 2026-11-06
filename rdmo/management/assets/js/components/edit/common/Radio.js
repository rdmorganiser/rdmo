import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty, isNil, uniqueId } from 'lodash'

import { getHelp, getLabel } from 'rdmo/management/assets/js/utils/forms'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const Radio = ({ element, field, options, onChange }) => {
  const meta = useSelector((state) => state.constants.meta)

  const label = getLabel(element, field, meta)
  const help = getHelp(element, field, meta)
  const errors = get(element, ['errors', field])

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className="mb-3">
      <label>{label}</label>

      <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2 gap-sm-5 py-2">
        {
          options.map((option, index) => {
            const radioId = uniqueId('radio-')

            return (
              <div key={index} className="form-check mb-0">
                <input
                  type="radio" id={radioId} disabled={element.read_only}
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
