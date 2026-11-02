import { useState } from 'react'

const useToggle = (initialValue = false) => {
  const [value, setValue] = useState(initialValue)
  const toggle = () => setValue((current) => !current)

  return [value, toggle]
}

export default useToggle
