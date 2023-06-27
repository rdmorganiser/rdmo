import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'
import ReactCodeMirror from '@uiw/react-codemirror'
import { html } from '@codemirror/lang-html'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const CodeMirror = ({ config, element, field, onChange }) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warnings = get(element, ['warnings', field]),
        errors = get(element, ['errors', field])

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warnings),
    'has-error': !isEmpty(errors)
  })

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <ReactCodeMirror className="codemirror form-control" id={id} value={value} extensions={[html()]}
                       onChange={(value) => onChange(field, value)} disabled={element.read_only} />

      {help && <p className="help-block">{help}</p>}

      {errors && <ul className="help-block list-unstyled">
        {errors.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

CodeMirror.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func
}

export default CodeMirror
