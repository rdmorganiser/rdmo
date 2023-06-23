import { useState } from 'react'

const useBool = (inital) => {
  const [value, setValue] = useState(inital)
  const toggleValue = () => setValue(!value)

  return [value, toggleValue]
}

export default useBool
