const getId = (element, field) => {
  if (element.model) {
    return `${element.model.replace('.', '-')}-${field}`
  } else {
    return field
  }
}

const getLabel = (config, element, field) => {
  if (config.meta && element.model && config.meta[element.model] && config.meta[element.model][field]) {
    return config.meta[element.model][field].verbose_name
  } else {
    return ''
  }
}

const getHelp = (config, element, field) => {
  if (config.meta && element.model && config.meta[element.model] && config.meta[element.model][field]) {
    return config.meta[element.model][field].help_text
  } else {
    return ''
  }
}

export { getId, getLabel, getHelp }
