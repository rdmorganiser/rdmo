import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isUndefined from 'lodash/isUndefined'

import Link from 'rdmo/core/assets/js/components/Link'

const EditLink = ({ element, verboseName, onClick }) => {
  const title = interpolate(gettext('Edit %s'), [verboseName])
  return <Link className="element-link fa fa-pencil" title={title} onClick={onClick} />
}

EditLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const AddLink = ({ element, verboseName, verboseNameAlt, onClick, onAltClick }) => {
  if (isUndefined(onAltClick)) {
    const title = interpolate(gettext('Add %s'), [verboseName])
    return <Link className="element-link fa fa-plus" title={title} onClick={onClick} />
  } else {
    const title = interpolate(gettext('Add %s or %s'), [verboseName, verboseNameAlt])
    return (
      <span className="dropdown">
        <a href="" className="element-link fa fa-plus" data-toggle="dropdown"></a>
        <ul className="dropdown-menu">
          <li>
            <Link href="" onClick={onClick}>
              {interpolate(gettext('Add %s'), [verboseName])}
            </Link>
          </li>
          <li>
            <Link href="" onClick={onAltClick}>
              {interpolate(gettext('Add %s'), [verboseNameAlt])}
            </Link>
          </li>
        </ul>
      </span>
    )
  }
}

AddLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  verboseName: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  onAltClick: PropTypes.func
}

const CopyLink = ({ element, verboseName, onClick }) => {
  const title = interpolate(gettext('Copy %s'), [verboseName])
  return <Link className="element-link fa fa-copy" title={title} onClick={onClick} />
}

CopyLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const AvailableLink = ({ element, verboseName, onClick }) => {
  const className = classNames({
    'element-link fa': true,
    'fa-toggle-on': element.available,
    'fa-toggle-off': !element.available,
    'disabled': element.locked
  })

  let title = interpolate(gettext('Make %s avaiable'), [verboseName])
  if (element.available) title = interpolate(gettext('Make %s unavaiable'), [verboseName])
  if (element.locked) title = gettext('Locked')

  return <Link className={className} title={title} onClick={onClick} />
}

AvailableLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const LockedLink = ({ element, verboseName, onClick }) => {
  const className = classNames({
    'element-link fa': true,
    'fa-lock text-danger': element.locked,
    'fa-unlock-alt': !element.locked
  })

  const title = element.locked ? interpolate(gettext('Unlock %s'), [verboseName])
                               : interpolate(gettext('Lock %s'), [verboseName])

  return <Link className={className} title={title} onClick={onClick} />
}

LockedLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const ExportLink = ({ element, verboseName }) => {
  const title = interpolate(gettext('Export %s as XML'), [verboseName])
  return (
    <a href={element.xml_url} className="element-link fa fa-download"
       title={title} target="_blank">
    </a>
  )
}

ExportLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired
}

const NestedLink = ({ element, verboseName, onClick }) => {
  const title = gettext('View nested')
  return <Link className="element-link fa fa-align-right flip" title={title} onClick={onClick} />
}

NestedLink.propTypes = {
  element: PropTypes.object.isRequired,
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const ExtendLink = ({ extend, onClick }) => {
  const className = classNames({
    'element-link fa': true,
    'fa-chevron-up': extend,
    'fa-chevron-down': !extend
  })

  const title = extend ? gettext('Show less')
                       : gettext('Show more')

  return <Link className={className} title={title} onClick={onClick} />
}

ExtendLink.propTypes = {
  extend: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired
}

const CodeLink = ({ className, uri, onClick }) => {
  return (
    <Link onClick={onClick}>
      <code className={className}>{uri}</code>
    </Link>
  )
}

CodeLink.propTypes = {
  className: PropTypes.string.isRequired,
  uri: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const ErrorLink = ({ element, onClick }) => {
  return (
    !isEmpty(element.errors) &&
    <Link className="element-link fa fa-warning text-danger" onClick={onClick} />
  )
}

ErrorLink.propTypes = {
  element: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
}


const WarningLink = ({ element, onClick }) => {
  return (
    !isEmpty(element.warnings) &&
    <Link className="element-link fa fa-warning text-warning" onClick={onClick} />
  )
}

WarningLink.propTypes = {
  element: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
}


const ShowLink = ({ element, onClick }) => {
  const title = element.show ? gettext('Hide') : gettext('Show')
  const className = classNames({
    'element-link fa': true,
    'fa-eye-slash': element.show,
    'fa-eye': !element.show
  })

  return <Link className={className} title={title} onClick={onClick} />
}

ShowLink.propTypes = {
  element: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
}

export { EditLink, CopyLink, AddLink, AvailableLink, LockedLink,
         NestedLink, ExportLink, ExtendLink, CodeLink, ErrorLink, WarningLink, ShowLink }
