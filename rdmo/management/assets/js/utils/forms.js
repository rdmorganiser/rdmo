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

export { getHelp, getId, getLabel }
