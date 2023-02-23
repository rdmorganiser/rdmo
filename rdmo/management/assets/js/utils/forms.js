const getId = (element, field) => {
  if (element.type) {
    return `${element.type}-${field}`
  } else {
    return field
  }
}

const getLabel = (config, element, field) => {
  if (config.meta && element.type && config.meta[element.type] && config.meta[element.type][field]) {
    return config.meta[element.type][field].verbose_name
  } else {
    return ''
  }
}

const getHelp = (config, element, field) => {
  if (config.meta && element.type && config.meta[element.type] && config.meta[element.type][field]) {
    return config.meta[element.type][field].help_text
  } else {
    return ''
  }
}

export { getId, getLabel, getHelp }
