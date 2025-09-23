import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isNil, invert } from 'lodash'

import { fetchElements } from '../../actions/elementActions'
import { uploadFile } from '../../actions/importActions'

import { elementTypes, elementModules } from '../../constants/elements'

import { buildApiPath, buildPath } from '../../utils/location'
import { getExportParams } from '../../utils/filter'

import Link from 'rdmo/core/assets/js/components/Link'

import { UploadForm } from '../common/Forms'

const ElementsSidebar = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const { elementType, elementId } = useSelector((state) => state.elements)

  const model = invert(elementTypes)[elementType]
  const exportUrl = isNil(elementId) ? buildApiPath(elementModules[model], elementType, 'export')
                                     : buildApiPath(elementModules[model], elementType, elementId, 'export')
  const exportParams = isNil(config.filter) ? '' : getExportParams(config.filter[elementType])

  return (
    <div className="elements-sidebar">
      <h2>Navigation</h2>

      <ul className="list-unstyled">
        <li>
          <Link href={buildPath('catalogs')}
                onClick={() => dispatch(fetchElements('catalogs'))}>{gettext('Catalogs')}</Link>
        </li>
        <li>
          <Link href={buildPath('sections')}
                onClick={() => dispatch(fetchElements('sections'))}>{gettext('Sections')}</Link>
        </li>
        <li>
          <Link href={buildPath('pages')}
                onClick={() => dispatch(fetchElements('pages'))}>{gettext('Pages')}</Link>
        </li>
        <li>
          <Link href={buildPath('questionsets')}
                onClick={() => dispatch(fetchElements('questionsets'))}>{gettext('Question sets')}</Link>
        </li>
        <li>
          <Link href={buildPath('questions')}
                onClick={() => dispatch(fetchElements('questions'))}>{gettext('Questions')}</Link>
        </li>
        <li>
          <Link href={buildPath('attributes')}
                onClick={() => dispatch(fetchElements('attributes'))}>{gettext('Attributes')}</Link>
        </li>
        <li>
          <Link href={buildPath('optionsets')}
                onClick={() => dispatch(fetchElements('optionsets'))}>{gettext('Option sets')}</Link>
        </li>
        <li>
          <Link href={buildPath('options')}
                onClick={() => dispatch(fetchElements('options'))}>{gettext('Options')}</Link>
        </li>
        <li>
          <Link href={buildPath('conditions')}
                onClick={() => dispatch(fetchElements('conditions'))}>{gettext('Conditions')}</Link>
        </li>
        <li>
          <Link href={buildPath('tasks')}
                onClick={() => dispatch(fetchElements('tasks'))}>{gettext('Tasks')}</Link>
        </li>
        <li>
          <Link href={buildPath('views')}
                onClick={() => dispatch(fetchElements('views'))}>{gettext('Views')}</Link>
        </li>
      </ul>

      <h2>Export</h2>

      <p className="text-muted">
        {gettext('Export all visible elements.')}
      </p>

      <ul className="list-unstyled">
        <li>
          <a href={`${exportUrl}?${exportParams}`}>{gettext('XML')}</a>
        </li>
        {
          [
            'catalogs',
            'sections',
            'pages',
            'questionsets',
            'questions',
            'optionsets',
            'conditions',
            'tasks'
          ].includes(elementType) && (
            <li>
              <a href={`${exportUrl}?full=true&${exportParams}`}>{gettext('XML (full)')}</a>
            </li>
          )
        }
      </ul>

      <ul className="list-unstyled">
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

      <p className="text-muted">
        {gettext('Import an RDMO XML file.')}
      </p>

      <UploadForm onSubmit={file => dispatch(uploadFile(file))} />
    </div>
  )
}

export default ElementsSidebar
