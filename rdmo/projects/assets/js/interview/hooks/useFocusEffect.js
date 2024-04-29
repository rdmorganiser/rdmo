import { useEffect } from 'react'

const useFocusEffect = (value, focus, ref) => {
  useEffect(() => {
    if (focus) {
      const timeout = setTimeout(() => {
        ref.current.focus()
      }, 100)

      return () => {
        // clears timeout before running the new effect
        clearTimeout(timeout)
      }
    }
  }, [value, focus])
}

export default useFocusEffect
