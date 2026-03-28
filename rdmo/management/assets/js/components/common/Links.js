import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isNil from 'lodash/isNil'
import isUndefined from 'lodash/isUndefined'

import Link from 'rdmo/core/assets/js/components/Link'
import LinkButton from 'rdmo/core/assets/js/components/LinkButton'

const NestedLink = ({ href, title, onClick, show = true }) => {
  return show && <Link href={href} className="element-link bi bi-list-nested" title={title} onClick={onClick} />
}

NestedLink.propTypes = {
  href: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  show: PropTypes.bool
}

const EditLink = ({ href, title, onClick, disabled = false }) => {
  return <Link href={href} className="element-link bi bi-pencil" title={title} onClick={onClick} disabled={disabled} />
}

EditLink.propTypes = {
  href: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
}

const CopyLink = ({ href, title, onClick }) => {
  return <Link href={href} className="element-link bi bi-copy" title={title} onClick={onClick} />
}

CopyLink.propTypes = {
  href: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

const AddLink = ({ title, altTitle, onClick, onAltClick, disabled }) => {
  if (isUndefined(onAltClick)) {
    return <LinkButton className="link bi bi-plus-lg" title={title} onClick={onClick} disabled={disabled} />
  } else {
    return (
      <span className="dropdown">
        <button type="button" className="link btn-link bi bi-plus-lg" data-toggle="dropdown"
          title={`${title}/${altTitle}`} aria-label={`${title}/${altTitle}`}>
        </button>
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
    'link bi': true,
    'bi-toggle-on': available,
    'bi-toggle-off': !available
  })

  return (
    <LinkButton className={className} title={locked ? gettext('Locked') : title}
      disabled={locked || disabled} onClick={onClick} />
  )
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
    'link bi': true,
    'bi-lock text-danger': locked,
    'bi-unlock': !locked
  })

  return <LinkButton className={className} title={title} onClick={onClick} disabled={disabled} />
}

LockedLink.propTypes = {
  locked: PropTypes.bool.isRequired,
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
}

const ToggleCurrentSiteLink = ({ hasCurrentSite, onClick, show }) => {
  const className = classNames({
    'link bi': true,
    'bi-plus-square': !hasCurrentSite,
    'bi-dash-square': hasCurrentSite,
  })
  const title = hasCurrentSite ? gettext('Remove your site') : gettext('Add your site')

  return  show && <LinkButton className={className} title={title} onClick={onClick} />
}

ToggleCurrentSiteLink.propTypes = {
  hasCurrentSite: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
  show: PropTypes.bool
}


const ShowElementsLink = ({ showElements, show, onClick }) => {
  const className = classNames({
    'link bi': true,
    'bi-chevron-down': showElements,
    'bi-chevron-up': !showElements
  })

  const title = showElements ? gettext('Hide elements') : gettext('Show elements')

  return show && <LinkButton className={className} title={title} onClick={onClick} />
}

ShowElementsLink.propTypes = {
  showElements: PropTypes.bool.isRequired,
  show: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired
}

const ExportLink = ({ exportUrl, title, exportFormats, csv = false, full = false }) => {
  return (
    <span className="dropdown">
      <button type="button" className="link link bi bi-download" data-bs-toggle="dropdown"
        title={title} aria-label={title}></button>
      <ul className="dropdown-menu dropdown-menu-end">
        <li className="dropdown-item">
          <a href={exportUrl}>{gettext('XML')}</a>
        </li>
        {
          full && (
            <li className="dropdown-item">
              <a href={exportUrl + '?full=true'}>{gettext('XML (full)')}</a>
            </li>
          )
        }
        <li><hr className="dropdown-divider" /></li>
        {
          csv && (
            <>
              <li className="dropdown-item">
                <a href={`${exportUrl}csvcomma/`}>
                  {gettext('CSV comma separated')}
                </a>
              </li>
              <li className="dropdown-item">
                <a href={`${exportUrl}csvsemicolon/`}>
                  {gettext('CSV semicolon separated')}
                </a>
              </li>
              <li><hr className="dropdown-divider" /></li>
            </>
          )
        }
        {
          exportFormats.map(([key, label], index) => (
            <li className="dropdown-item" key={index}>
              <a href={`${exportUrl}${key}/`}
                target={['pdf', 'html'].includes(key) ? '_blank' : '_self'}
                rel="noreferrer">{label}</a>
            </li>
          ))
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
  const className = classNames('element-link bi ms-1', {
    'bi-chevron-up': extend,
    'bi-chevron-down': !extend
  })

  const title = extend ? gettext('Show less') : gettext('Show more')

  return <Link className={className} title={title} onClick={onClick} />
}

ExtendLink.propTypes = {
  extend: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired
}

const CodeLink = ({ className, type, uri, href, onClick, order }) => {
  return (
    <span className={classNames('d-flex gap-2', className)}>
      <Link href={href} onClick={onClick}>
        <code className={`code-${type}`}>{uri}</code>
      </Link>
      {
        !isNil(order) && (
          <span>
            <code className="code-order">{order}</code>
          </span>
        )
      }
    </span>
  )
}

CodeLink.propTypes = {
  className: PropTypes.string,
  type: PropTypes.string.isRequired,
  uri: PropTypes.string.isRequired,
  href: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  order: PropTypes.number
}

const ErrorLink = ({ onClick }) => {
  return <Link className="element-link bi bi-exclamation-triangle text-danger" onClick={onClick} />
}

ErrorLink.propTypes = {
  onClick: PropTypes.func.isRequired
}

const WarningLink = ({ onClick }) => {
  return <Link className="element-link bi bi-exclamation-triangle text-warning" onClick={onClick} />
}

WarningLink.propTypes = {
  onClick: PropTypes.func.isRequired
}

const ShowLink = ({ show = false, onClick }) => {
  const title = show ? gettext('Hide') : gettext('Show')
  const className = classNames({
    'element-link bi': true,
    'bi-chevron-down': !show,
    'bi-chevron-up': show
  })

  return <Link className={className} title={title} onClick={onClick} />
}

ShowLink.propTypes = {
  show: PropTypes.bool,
  onClick: PropTypes.func.isRequired
}

export {
  AddLink,
  AvailableLink,
  CodeLink,
  CopyLink,
  EditLink,
  ErrorLink,
  ExportLink,
  ExtendLink,
  LockedLink,
  NestedLink,
  ShowElementsLink,
  ShowLink,
  ToggleCurrentSiteLink,
  WarningLink
}
