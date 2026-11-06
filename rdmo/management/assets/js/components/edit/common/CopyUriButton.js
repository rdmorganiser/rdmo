import React, { useEffect, useRef, useState } from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import LinkButton from 'rdmo/core/assets/js/components/LinkButton'

const CopyUriButton = ({ uri }) => {
  const [copied, setCopied] = useState(false)
  const timeout = useRef(null)

  useEffect(() => () => clearTimeout(timeout.current), [])

  const handleClick = () => {
    navigator.clipboard?.writeText(uri).then(() => {
      setCopied(true)
      clearTimeout(timeout.current)
      timeout.current = setTimeout(() => setCopied(false), 1500)
    }).catch(() => {})
  }

  return (
    <LinkButton
      className={copied ? 'bi bi-clipboard-check' : 'bi bi-clipboard'}
      title={copied ? gettext('URI copied') : gettext('Copy URI')}
      disabled={isEmpty(uri)}
      onClick={handleClick} />
  )
}

CopyUriButton.propTypes = {
  uri: PropTypes.string
}

export default CopyUriButton
