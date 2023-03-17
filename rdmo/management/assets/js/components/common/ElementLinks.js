import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'


const EditLink = ({ element, verboseName, onClick }) => {
  const handleClick = (event) => {
    event.preventDefault()
    onClick()
  }

  const title = interpolate(gettext('Edit %s'), [verboseName])

  return (
    <a href="" className="fa fa-pencil"
       title={title}
       onClick={event => handleClick(event)}>
    </a>
  )
}

EditLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}


const AvailableLink = ({ element, verboseName, onClick }) => {
  const handleClick = (event) => {
    event.preventDefault()
    onClick()
  }

  const className = classNames({
    'fa': true,
    'fa-toggle-on': element.available,
    'fa-toggle-off': !element.available,
    'disabled': element.locked
  })

  let title = interpolate(gettext('Make %s avaiable'), [verboseName])
  if (element.available) title = interpolate(gettext('Make %s unavaiable'), [verboseName])
  if (element.locked) title = gettext('Locked')

  return (
    <a href="" className={className}
       title={title}
       onClick={event => handleClick(event)}>
    </a>
  )
}

AvailableLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const LockedLink = ({ element, verboseName, onClick }) => {
  const handleClick = (event) => {
    event.preventDefault()
    onClick()
  }

  const className = classNames({
    'fa': true,
    'fa fa-lock': element.locked,
    'fa fa-unlock-alt': !element.locked
  })

  const title = element.locked ? interpolate(gettext('Unlock %s'), [verboseName])
                               : interpolate(gettext('Lock %s'), [verboseName])

  return (
    <a href="" className={className}
       title={title}
       onClick={event => handleClick(event)}>
    </a>
  )
}

LockedLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const ExportLink = ({ element, verboseName }) => {
  const title = interpolate(gettext('Export %s as XML'), [verboseName])

  return (
    <a href={element.xml_url} className="fa fa-download"
       title={title} target="_blank">
    </a>
  )
}

ExportLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired
}


const NestedLink = ({ element, verboseName, onClick }) => {
  const handleClick = (event) => {
    event.preventDefault()
    onClick()
  }

  const title = gettext('View nested')

  return (
    <a href="" className="fa fa-align-right flip"
       title={title}
       onClick={event => handleClick(event)}>
    </a>
  )
}

NestedLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}


export { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink }
