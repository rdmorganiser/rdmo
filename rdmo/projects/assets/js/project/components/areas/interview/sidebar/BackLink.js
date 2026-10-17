import React from 'react'

import LocationLink from '../../../helper/LocationLink'

const BackLink = () => (
  <div className="mb-2">
    <LocationLink title={gettext('Navigate to back to overview')} location={{ area: 'interview' }}>
      <i className="bi bi-arrow-left me-1"></i> {gettext('Back to overview')}
    </LocationLink>
  </div>
)

export default BackLink
