import React, { useEffect, useRef, useState } from 'react'
import PropTypes from 'prop-types'
import { createPortal } from 'react-dom'
import { Tooltip as BootstrapTooltip } from 'bootstrap'

const Tooltip = ({ title, children, placement = 'bottom', tooltipProps = {} }) => {
  const ref = useRef(null)
  const [container] = useState(() => document.createElement('div'))

  useEffect(() => {
    if (!title || !ref.current) return

    BootstrapTooltip.getInstance(ref.current)?.dispose()

    const t = new BootstrapTooltip(ref.current, {
      title: container,
      placement,
      html: true,
      delay: 200,
      ...tooltipProps
    })
    return () => t.dispose()
  }, [Boolean(title), placement, JSON.stringify(tooltipProps)])

  return (
    <>
      {React.cloneElement(children, { ref })}
      {title && createPortal(title, container)}
    </>
  )
}

Tooltip.propTypes = {
  title: PropTypes.node.isRequired,
  children: PropTypes.node.isRequired,
  placement: PropTypes.string,
  tooltipProps: PropTypes.object
}

export default Tooltip
