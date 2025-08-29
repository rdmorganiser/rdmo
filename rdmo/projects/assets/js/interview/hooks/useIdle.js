import { useState, useEffect } from 'react'

const useIdle = (dependencies) => {
  const [idle, setIdle] = useState(true)

  useEffect(() => setIdle(true), dependencies)

  return [idle, setIdle]
}

export default useIdle
