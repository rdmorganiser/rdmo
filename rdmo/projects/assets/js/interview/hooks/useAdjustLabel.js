import { useEffect } from 'react'

const useAdjustLabel = (ref) => {
  useEffect(() => {
    if (ref.current) {
      // find the .buttons node and get it's width
      const buttons = ref.current.querySelector('.buttons')
      const buttonsWidth = buttons.offsetWidth

      // find the first label for a radio or checkbox and adjust the right padding
      const label = ref.current.querySelector('.radio:first-child label, .checkbox:first-child label')
      label.style.paddingRight = `${label.style.paddingRight + buttonsWidth}px`
    }
  }, [])
}

export default useAdjustLabel
