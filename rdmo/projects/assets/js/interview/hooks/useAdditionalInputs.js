import { useState, useEffect } from 'react'
import { get, isNil } from 'lodash'

const useAdditionalInputs = (value, options) => {
  const [additionalInputs, setAdditionalInputs] = useState({})

  useEffect(() => {
    if (isNil(value)) {
      setAdditionalInputs({})
    } else {
      setAdditionalInputs(options.reduce((additionalInputs, option) => {
        if (value.option == option.id) {
          additionalInputs[option.id] = value.text
        }
        return additionalInputs
      }, {}))
    }
  }, [get(value, 'id'), get(value, 'text'), get(value, 'option'), get(value, 'external_id')])

  return [
    (option) => additionalInputs[option.id] || '',
    (option, additionalInput) => setAdditionalInputs({
      ...additionalInputs, [option.id]: additionalInput
    })
  ]
}

export default useAdditionalInputs
