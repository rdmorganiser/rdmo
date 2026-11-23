import React from 'react'

const getId = (element, field) => {
  if (element.model) {
    return `${element.model.replace('.', '-')}-${field}`
  } else {
    return field
  }
}

const getLabel = (element, field, meta) => {
  if (meta && element.model && meta[element.model] && meta[element.model][field]) {
    return meta[element.model][field].verbose_name
  } else {
    return ''
  }
}

const getHelp = (element, field, meta) => {
  if (meta && element.model && meta[element.model] && meta[element.model][field]) {
    return meta[element.model][field].help_text
  } else {
    return ''
  }
}

const formatOptionLabel = ({ label }, { context }) => {
  const parts = label.split('/')

  if (context === 'menu') {
    // insert <wbr> at /
    return (
      <span>
        {
          parts.map((part, index) => (
            index === 0 ? part : [<wbr key={index} />, '/', part]
          ))
        }
      </span>
    )
  }

  // show less of the uri on small screens
  const tailLength = window.matchMedia('(min-width: 576px)').matches ? 3 : 1

  if (parts.length > tailLength) {
    const head = `${parts.slice(0, -tailLength).join('/')}`
    const tail = `/${parts.slice(-tailLength).join('/')}`
    return (
      <span className="truncate-option-label">
        <span className="truncate-option-label-head">{head}</span>
        <span className="truncate-option-label-tail">{tail}</span>
      </span>
    )
  } else {
    return label
  }
}

export { formatOptionLabel, getHelp, getId, getLabel }
