import React from 'react'
import PropTypes from 'prop-types'
import isNil from 'lodash/isNil'
import invert from 'lodash/invert'

import { elementTypes, elementModules } from '../../constants/elements'

import { buildPath } from '../../utils/location'
import { getExportParams } from '../../utils/filter'

import Link from 'rdmo/core/assets/js/components/Link'

import { UploadForm } from '../common/Forms'

const ElementsSidebar = ({ config, elements, elementActions, importActions }) => {
  const { elementType, elementId } = elements

  const model = invert(elementTypes)[elementType]
  const exportUrl = isNil(elementId) ? buildPath(config.apiUrl, elementModules[model], elementType, 'export')
                                     : buildPath(config.apiUrl, elementModules[model], elementType, elementId, 'export')
  const exportParams = getExportParams(config.filter[elementType])

  return (
    <div className="elements-sidebar">
      <h2>Navigation</h2>

      <ul className="list-unstyled">
        <li>
          <Link href={buildPath(config.baseUrl, 'catalogs')}
                onClick={() => elementActions.fetchElements('catalogs')}>{gettext('Catalogs')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'sections')}
                onClick={() => elementActions.fetchElements('sections')}>{gettext('Sections')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'pages')}
                onClick={() => elementActions.fetchElements('pages')}>{gettext('Pages')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'questionsets')}
                onClick={() => elementActions.fetchElements('questionsets')}>{gettext('Question sets')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'questions')}
                onClick={() => elementActions.fetchElements('questions')}>{gettext('Questions')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'attributes')}
                onClick={() => elementActions.fetchElements('attributes')}>{gettext('Attributes')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'optionsets')}
                onClick={() => elementActions.fetchElements('optionsets')}>{gettext('Option sets')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'options')}
                onClick={() => elementActions.fetchElements('options')}>{gettext('Options')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'conditions')}
                onClick={() => elementActions.fetchElements('conditions')}>{gettext('Conditions')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'tasks')}
                onClick={() => elementActions.fetchElements('tasks')}>{gettext('Tasks')}</Link>
        </li>
        <li>
          <Link href={buildPath(config.baseUrl, 'views')}
                onClick={() => elementActions.fetchElements('views')}>{gettext('Views')}</Link>
        </li>
      </ul>

      <h2>Export</h2>

      <ul className="list-unstyled">
        <li>
          <a href={`${exportUrl}?${exportParams}`}>{gettext('XML')}</a>
        </li>
        {
          elementType == 'attributes' && <>
            <li>
              <a href={`${exportUrl}csvcomma/?${exportParams}`}>
                {gettext('CSV comma separated')}
              </a>
            </li>
            <li>
              <a href={`${exportUrl}csvsemicolon/?${exportParams}`}>
                {gettext('CSV semicolon separated')}
              </a>
            </li>
          </>
        }
        {
          config.settings.export_formats &&
          config.settings.export_formats.map(([key, label], index) => <li key={index}>
            <a href={`${exportUrl}${key}/?${exportParams}`}
               target={['pdf', 'html'].includes(key) ? '_blank' : '_self'}
               rel="noreferrer">{label}</a>
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
