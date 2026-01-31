import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const UriPrefix = ({ element, field, onChange }) => {
  const { meta, settings } = useSelector((state) => state.config)

  const id = getId(element, field),
        label = getLabel(element, field, meta),
        help = getHelp(element, field, meta),
        errors = get(element, ['errors', field])

  const className = classNames('form-control', {
    'is-invalid': !isEmpty(errors)
  })

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className="mb-3">
      <label className="form-label" htmlFor={id}>{label}</label>

      <div className="input-group">
        <input type="text" id={id} className={className} disabled={element.read_only}
               value={value} onChange={event => onChange(field, event.target.value)} />

        <button type="button" className="btn btn-light border" disabled={element.read_only}
          title={gettext('Insert default URI Prefix')} aria-label={gettext('Insert default URI Prefix')}
          onClick={() => onChange(field, settings.default_uri_prefix)}>
          <span className="bi bi-magic"></span>
        </button>
      </div>

      <ErrorList errors={errors} />
      <HelpText help={help} />
    </div>
  )
}

UriPrefix.propTypes = {
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func
}

export default UriPrefix
