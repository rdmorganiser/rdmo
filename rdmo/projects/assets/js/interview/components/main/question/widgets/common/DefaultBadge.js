import React from 'react'

const DefaultBadge = () => {
  return (
    <div className="badge badge-default" title={gettext('This is a default answer that can be customized.')}>
      {gettext('Default')}
    </div>
  )
}

export default DefaultBadge
