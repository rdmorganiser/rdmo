const initValues = (values, sets, page) => {
  console.log(values, sets, page)
  return values
}


const replaceValue = (values, value) => {
  const newValues = [...values]
  const index = newValues.findIndex(v => {
    return v.id == value.id
  })
  if (index > -1) {
    newValues[index] = value
  } else {
    newValues.push(value)
  }

  return newValues
}

const removeValue = (values, value) => {
  return values.filter((v) => (v.id != value.id))
}

export { initValues, replaceValue, removeValue }
