import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import classNames from 'classnames'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { getHelp, getId, getLabel } from 'rdmo/management/assets/js/utils/forms'

import ErrorList from './ErrorList'
import HelpText from './HelpText'
import { html } from '@codemirror/lang-html'
import { EditorView } from '@codemirror/view'
import ReactCodeMirror from '@uiw/react-codemirror'

const CodeMirror = ({ element, field, onChange }) => {
  const { meta } = useSelector((state) => state.config)

  const id = getId(element, field),
    label = getLabel(element, field, meta),
    help = getHelp(element, field, meta),
    errors = get(element, ['errors', field])

  const className = classNames('codemirror form-control', {
    'is-invalid': !isEmpty(errors),
    'disabled': element.read_only
  })

  const value = isNil(element[field]) ? '' : element[field]

  const extensions = [html()]

  if (element.read_only) {
    extensions.push(EditorView.editable.of(false))
  }

  return (
    <div className="mb-3">
      <label className="control-label" htmlFor={id}>{label}</label>

      <ReactCodeMirror className={className} id={id} value={value} extensions={extensions}
        onChange={(value) => onChange(field, value)} disabled={element.read_only} />

      <ErrorList errors={errors} />
      <HelpText help={help} />
    </div>
  )
}

CodeMirror.propTypes = {
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func
}

export default CodeMirror
