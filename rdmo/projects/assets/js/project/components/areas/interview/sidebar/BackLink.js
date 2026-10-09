import React from 'react'

import LocationLink from '../../../helper/LocationLink'

const BackLink = () => (
  <LocationLink title={gettext('Navigate to back to overview')} location={{ area: 'interview' }}>
    <i className="bi bi-arrow-left"></i>
    <span className="d-none d-lg-inline ms-2">
      {gettext('Back to overview')}
    </span>
  </LocationLink>
)

export default BackLink
