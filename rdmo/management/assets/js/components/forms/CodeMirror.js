import React, { Component} from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import ReactCodeMirror from '@uiw/react-codemirror';
import { html } from '@codemirror/lang-html';

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const CodeMirror = ({ config, element, field, warnings, errors, rows, onChange }) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warningList = warnings[field],
        errorList = errors[field]

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warningList),
    'has-error': !isEmpty(errorList)
  })

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <ReactCodeMirror className="codemirror form-control" id={id} value={value} extensions={[html()]}
                       onChange={(value, viewUpdate) => onChange(field, value)} />

      {help && <p className="help-block">{help}</p>}

      {errorList && <ul className="help-block list-unstyled">
        {errorList.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

CodeMirror.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  rows: PropTypes.number,
  onChange: PropTypes.func
}

export default CodeMirror
