import React, { useRef, useEffect } from 'react'
import PropTypes from 'prop-types'
import { components } from 'react-select'

const SelectValueContainer = (props) => {
  const ref = useRef(null)

  useEffect(() => {
    if (!ref.current) return

    const links = ref.current.querySelectorAll('a')
    const handlers = []

    links.forEach((link) => {
      const handler = (e) => e.stopPropagation()

      link.addEventListener('mousedown', handler)
      link.setAttribute('target', '_blank')
      link.setAttribute('rel', 'noopener noreferrer')

      handlers.push({ link, handler })
    })

    return () => {
      handlers.forEach(({ link, handler }) => {
        link.removeEventListener('mousedown', handler)
      })
    }
  }, [])

  return (
    <components.ValueContainer {...props}>
      <span ref={ref} style={{ display: 'inline-flex', alignItems: 'center' }}>
        {props.children}
      </span>
    </components.ValueContainer>
  )
}

SelectValueContainer.propTypes = {
  children: PropTypes.node
}

export default SelectValueContainer
