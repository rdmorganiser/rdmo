import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import isUndefined from 'lodash/isUndefined'

import Link from 'rdmo/core/assets/js/components/Link'
import LinkButton from 'rdmo/core/assets/js/components/LinkButton'

const NestedLink = ({ href, title, onClick, show=true }) => {
  return show && <Link href={href} className="element-link fa fa-align-right flip" title={title} onClick={onClick} />
}

NestedLink.propTypes = {
  href: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  show: PropTypes.bool
}

const EditLink = ({ href, title, onClick }) => {
  return <Link href={href} className="element-link fa fa-pencil" title={title} onClick={onClick} />
}

EditLink.propTypes = {
  href: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const CopyLink = ({ href, title, onClick }) => {
  return <Link href={href} className="element-link fa fa-copy" title={title} onClick={onClick} />
}

CopyLink.propTypes = {
  href: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const AddLink = ({ title, altTitle, onClick, onAltClick, disabled }) => {
  if (isUndefined(onAltClick)) {
    return <LinkButton className="element-btn-link fa fa-plus" title={title} onClick={onClick} disabled={disabled} />
  } else {
    return (
      <span className="dropdown">
        <button className="element-btn-link btn-link fa fa-plus" data-toggle="dropdown"></button>
        <ul className="dropdown-menu">
          <li onClick={onClick}>
            <Link href="" onClick={onClick}>{title}</Link>
          </li>
          <li>
            <Link href="" onClick={onAltClick}>{altTitle}</Link>
          </li>
        </ul>
      </span>
    )
  }
}

AddLink.propTypes = {
  title: PropTypes.string.isRequired,
  altTitle: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  onAltClick: PropTypes.func,
  disabled: PropTypes.bool
}

const AvailableLink = ({ available, locked, title, onClick, disabled }) => {
  const className = classNames({
    'element-btn-link fa': true,
    'fa-toggle-on': available,
    'fa-toggle-off': !available
  })

  return <LinkButton className={className} title={locked ? gettext('Locked') : title}
                     disabled={locked || disabled} onClick={onClick} />
}

AvailableLink.propTypes = {
  available: PropTypes.bool.isRequired,
  locked: PropTypes.bool.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
}

const LockedLink = ({ locked, title, onClick, disabled }) => {
  const className = classNames({
    'element-btn-link fa': true,
    'fa-lock text-danger': locked,
    'fa-unlock-alt': !locked
  })

  return <LinkButton className={className} title={title} onClick={onClick} disabled={disabled} />
}

LockedLink.propTypes = {
  locked: PropTypes.bool.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
}

const ToggleCurrentSiteLink = ({ has_current_site, locked, onClick, disabled }) => {
  const className = classNames({
    'element-btn-link fa': true,
    'fa-plus-square-o': !has_current_site,
    'fa-minus-square-o': has_current_site,
  })
  const title = has_current_site ? gettext('Remove your site'): gettext('Add your site')

  return  <LinkButton className={className} title={locked ? gettext('Locked') : title}
                     disabled={locked || disabled} onClick={onClick} />
}

ToggleCurrentSiteLink.propTypes = {
  has_current_site: PropTypes.bool.isRequired,
  locked: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
}


const ShowElementsLink = ({ showElements, show, onClick }) => {
  const className = classNames({
    'element-btn-link fa': true,
    'fa-chevron-down': showElements,
    'fa-chevron-up': !showElements
  })

  const title = showElements ? gettext('Hide elements') : gettext('Show elements')

  return show && <LinkButton className={className} title={title} onClick={onClick} />
}

ShowElementsLink.propTypes = {
  showElements: PropTypes.bool.isRequired,
  show: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired
}

const ExportLink = ({ exportUrl, title, exportFormats, csv=false, full=false }) => {
  return (
    <span className="dropdown">
      <button className="element-btn-link btn-link fa fa-download" title={title} data-toggle="dropdown"></button>
      <ul className="dropdown-menu">
        <li><a href={exportUrl}>{gettext('XML')}</a></li>
        {
          full && <li><a href={exportUrl + '?full=true'}>{gettext('XML (full)')}</a></li>
        }
        <li role="separator" className="divider"></li>
        {
          csv && <>
            <li><a href={`${exportUrl}csvcomma/`}>
              {gettext('CSV comma separated')}
            </a></li>
            <li><a href={`${exportUrl}csvsemicolon/`}>
              {gettext('CSV semicolon separated')}
            </a></li>
            <li role="separator" className="divider"></li>
          </>
        }
        {
          exportFormats.map(([key, label], index) => <li key={index}>
            <a href={`${exportUrl}${key}/`}
               target={['pdf', 'html'].includes(key) ? '_blank' : '_self'}
               rel="noreferrer">{label}</a>
          </li>)
        }
      </ul>
    </span>
  )
}

ExportLink.propTypes = {
  exportUrl: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  exportFormats: PropTypes.array,
  csv: PropTypes.bool,
  full: PropTypes.bool
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

const CodeLink = ({ className, uri, onClick, order }) => {
  return (
    <>
      <Link onClick={onClick}>
        <code className={className}>{uri}</code>
      </Link>
      {!isNil(order) ? (
        <>{' '}<code className="code-order ng-binding">{order}</code></>
      ) : null}
    </>
  )
}

CodeLink.propTypes = {
  className: PropTypes.string.isRequired,
  uri: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  order: PropTypes.number
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

export { EditLink, CopyLink, AddLink, AvailableLink, ToggleCurrentSiteLink, LockedLink, ShowElementsLink,
         NestedLink, ExportLink, ExtendLink, CodeLink, ErrorLink, WarningLink, ShowLink }
