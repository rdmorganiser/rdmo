import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isUndefined from 'lodash/isUndefined'

import Link from 'rdmo/core/assets/js/components/Link'

import { elementModules } from '../../constants/elements'

const EditLink = ({ verboseName, onClick }) => {
  const title = interpolate(gettext('Edit %s'), [verboseName])
  return <Link className="element-link fa fa-pencil" title={title} onClick={onClick} />
}

EditLink.propTypes = {
  verboseName: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const AddLink = ({ verboseName, verboseNameAlt, onClick, onAltClick }) => {
  let title
  if (isUndefined(onAltClick)) {
    title = interpolate(gettext('Add %s'), [verboseName])
    return <Link className="element-link fa fa-plus" title={title} onClick={onClick} />
  } else {
    title = interpolate(gettext('Add %s or %s'), [verboseName, verboseNameAlt])
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
  verboseName: PropTypes.string.isRequired,
  verboseNameAlt: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  onAltClick: PropTypes.func
}

const CopyLink = ({ verboseName, onClick }) => {
  const title = interpolate(gettext('Copy %s'), [verboseName])
  return <Link className="element-link fa fa-copy" title={title} onClick={onClick} />
}

CopyLink.propTypes = {
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

const ExportLink = ({ element, elementType, verboseName, exportFormats }) => {
  const title = interpolate(gettext('Export %s'), [verboseName])
  const url = `/api/v1/${elementModules[elementType]}/${elementType}`
  return (
    <span className="dropdown">
      <a href="" className="element-link fa fa-download" title={title} data-toggle="dropdown"></a>
      <ul className="dropdown-menu">
        <li><a href={`${url}/${element.id}/export/`}>{gettext('XML')}</a></li>
        <li role="separator" className="divider"></li>
        {
          elementType == 'attributes' && <>
            <li><a href={`${url}/${element.id}/export/csvcomma/`}>
              {gettext('CSV comma separated')}
            </a></li>
            <li><a href={`${url}/${element.id}/export/csvsemicolon/`}>
              {gettext('CSV semicolon separated')}
            </a></li>
            <li role="separator" className="divider"></li>
          </>
        }
        {
          exportFormats.map(([key, label], index) => <li key={index}>
            <a href={`${url}/${element.id}/export/${key}/`}
               target={['pdf', 'html'].includes(key) ? '_blank' : '_self'}
               rel="noreferrer">{label}</a>
          </li>)
        }
      </ul>
    </span>
  )
}

ExportLink.propTypes = {
  element: PropTypes.object.isRequired,
  elementType: PropTypes.string.isRequired,
  verboseName: PropTypes.string.isRequired,
  exportFormats: PropTypes.array
}

const NestedLink = ({ onClick }) => {
  const title = gettext('View nested')
  return <Link className="element-link fa fa-align-right flip" title={title} onClick={onClick} />
}

NestedLink.propTypes = {
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
