import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import Page from './Page'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink, ExportLink, CodeLink } from '../common/Links'
import { Drag, Drop } from '../common/DragAndDrop'

const Section = ({ config, section, elementActions, display='list', filter=null, indent=0 }) => {

  const showElement = filterElement(filter, section)

  const editUrl = buildPath(config.baseUrl, 'sections', section.id)
  const copyUrl = buildPath(config.baseUrl, 'sections', section.id, 'copy')
  const nestedUrl = buildPath(config.baseUrl, 'sections', section.id, 'nested')
  const exportUrl = buildPath('/api/v1/', 'questions', 'sections', section.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('sections', section.id)
  const fetchCopy = () => elementActions.fetchElement('sections', section.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('sections', section.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('sections', {...section, locked: !section.locked })

  const createPage = () => elementActions.createElement('pages', { section })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <NestedLink title={gettext('View section nested')} href={nestedUrl} onClick={fetchNested} />
        <EditLink title={gettext('Edit section')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy section')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add page')} onClick={createPage} />
        <LockedLink title={section.locked ? gettext('Unlock section')
                                          : gettext('Lock section')}
                    locked={section.locked} onClick={toggleLocked} />
        <ExportLink title={gettext('Export section')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
        {display == 'nested' && <Drag element={section} />}
      </div>
      <div>
        <p>
          <strong>{gettext('Section')}{': '}</strong> {section.title}
        </p>
        {
          config.display.uri.sections &&
          <CodeLink className="code-questions" uri={section.uri} onClick={() => fetchEdit()} />
        }
        <ElementErrors element={section} />
      </div>
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          { elementNode }
        </li>
      )
    case 'nested':
      return (
        <>
          {
            showElement && config.display.elements.sections && (
              <Drop element={section} elementActions={elementActions}>
                <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
                  <div className="panel-heading">
                    { elementNode }
                  </div>
                </div>
              </Drop>
            )
          }
          {
            !isEmpty(section.elements) &&
            <Drop element={section.elements[0]} elementActions={elementActions} indent={indent + 1} mode="before" />
          }
          {
            section.elements.map((page, index) => (
              <Page key={index} config={config} page={page} elementActions={elementActions}
                    display="nested" filter={filter} indent={indent + 1} />
            ))
          }
          <Drop element={section} elementActions={elementActions} indent={indent} mode="after" />
        </>
      )
    case 'plain':
      return elementNode
  }
}

Section.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.object,
  indent: PropTypes.number
}

export default Section
