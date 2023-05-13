import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty'

import { buildPath } from '../../utils/location'
import { elementModules } from '../../constants/elements'

import Link from 'rdmo/core/assets/js/components/Link'

import { UploadForm } from '../common/Forms'

const ElementsSidebar = ({ config, elements, elementActions, importActions }) => {
  const { elementType } = elements
  const exportUrl = `/api/v1/${elementModules[elementType]}/${elementType}/export/`

  return (
    <div className="elements-sidebar">
      <h2>Navigation</h2>

      <ul className="list-unstyled">
        <li>
          <Link href={buildPath(config.baseUrl, 'catalogs')}
                onClick={() => elementActions.fetchElements('catalogs')}>Catalogs</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'sections')}
                onClick={() => elementActions.fetchElements('sections')}>Sections</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'pages')}
                onClick={() => elementActions.fetchElements('pages')}>Pages</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'questionsets')}
                onClick={() => elementActions.fetchElements('questionsets')}>Question sets</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'questions')}
                onClick={() => elementActions.fetchElements('questions')}>Questions</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'attributes')}
                onClick={() => elementActions.fetchElements('attributes')}>Attributes</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'optionsets')}
                onClick={() => elementActions.fetchElements('optionsets')}>Option sets</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'options')}
                onClick={() => elementActions.fetchElements('options')}>Options</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'conditions')}
                onClick={() => elementActions.fetchElements('conditions')}>Conditions</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'tasks')}
                onClick={() => elementActions.fetchElements('tasks')}>Tasks</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'views')}
                onClick={() => elementActions.fetchElements('views')}>Views</Link>
        </li>
      </ul>

      <h2>Export</h2>

      <ul className="list-unstyled">
        <li>
          <a href={exportUrl}>{gettext('XML')}</a>
        </li>
        {
          elementType == 'attributes' && <>
            <li>
              <a href={`${exportUrl}csvcomma/`}>
                {gettext('CSV comma separated')}
              </a>
            </li>
            <li>
              <a href={`${exportUrl}csvsemicolon/`}>
                {gettext('CSV semicolon separated')}
              </a>
            </li>
          </>
        }
        {
          config.settings.export_formats &&
          config.settings.export_formats.map(([key, label], index) => <li key={index}>
            <a href={`${exportUrl}${key}/`}
               target={['pdf', 'html'].includes(key) ? '_blank' : '_self'}>{label}</a>
          </li>)
        }
      </ul>

      <h2>Import</h2>

      <UploadForm onSubmit={file => importActions.uploadFile(file)} />
    </div>
  )
}

ElementsSidebar.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ElementsSidebar
