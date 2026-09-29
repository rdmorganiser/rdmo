import React from 'react'

import Link from '../../../helper/Link'

const Back = () => (
  <Link location={{ area: 'interview' }}>
    <i className="bi bi-arrow-left"></i>
    <span className="d-none d-lg-inline ms-2">
      {gettext('Back to overview')}
    </span>
  </Link>
)

export default Back
