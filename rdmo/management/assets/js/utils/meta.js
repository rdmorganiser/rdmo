const getLabel = (config, elementType, field) => {
  if (config.meta && config.meta[elementType] && config.meta[elementType][field]) {
    return config.meta[elementType][field].verbose_name
  } else {
    return ''
  }
}

const getHelp = (config, elementType, field) => {
  if (config.meta && config.meta[elementType] && config.meta[elementType][field]) {
    return config.meta[elementType][field].help_text
  } else {
    return ''
  }
}

export { getLabel, getHelp }
