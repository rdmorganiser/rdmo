import { useState } from 'react'

const useBool = (initial) => {
  const [value, setValue] = useState(initial)
  const toggleValue = () => setValue(!value)

  return [value, toggleValue]
}

export default useBool
