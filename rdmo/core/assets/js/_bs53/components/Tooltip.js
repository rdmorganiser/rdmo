import React, { useEffect, useRef } from 'react'
import { renderToString } from 'react-dom/server'
import PropTypes from 'prop-types'
import { Tooltip as BootstrapTooltip } from 'bootstrap'

const Tooltip = ({ title, children, placement = 'bottom', tooltipProps = {} }) => {
  const ref = useRef(null)

  useEffect(() => {
    if (title) {
      // console.log(renderToString(title))
      const t = new BootstrapTooltip(ref.current, {
        title: renderToString(title),
        placement,
        html: true,
        delay: 200,
        ...tooltipProps
      })
      return () => t.dispose()
    }
  }, [title])

  return React.cloneElement(children, { ref })
}

Tooltip.propTypes = {
  title: PropTypes.node.isRequired,
  children: PropTypes.node.isRequired,
  placement: PropTypes.string,
  tooltipProps: PropTypes.object,
}

export default Tooltip
