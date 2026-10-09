import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { staticUrl } from 'rdmo/core/assets/js/utils/meta'

const Img = ({ src, alt, className }) => {
  return !isEmpty(src) && (
    <img src={staticUrl + src} alt={alt} className={className} />
  )
}

Img.propTypes = {
  src: PropTypes.string,
  alt: PropTypes.string,
  className: PropTypes.string,
}

export default Img
