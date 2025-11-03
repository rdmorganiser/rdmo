import { useEffect } from 'react'

const useAdjustLabel = (ref) => {
  useEffect(() => {
    if (ref.current) {
      // find the .buttons node and get it's width
      const buttonsWidth = ref.current.classList.contains('checkbox') ? (
        // for the checkbox widget, the parent of the parent is the buttons-wrapper
        ref.current.parentElement.parentElement.querySelector('.buttons').offsetWidth
      ) : (
        ref.current.querySelector('.buttons').offsetWidth
      )

      // find the first label for a radio or checkbox and adjust the right padding
      const label = ref.current.querySelector('.radio:first-child label, .checkbox:first-child label')
      if (label) {
        label.style.paddingRight = `${label.style.paddingRight + buttonsWidth}px`
      }
    }
  }, [ref.current])
}

export default useAdjustLabel
