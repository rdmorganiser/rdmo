import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import { filterElement } from '../../utils/filter'

import Page from './Page'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink, ExportLink, CodeLink } from '../common/Links'
import { Drag, Drop } from '../common/DragAndDrop'

const Section = ({ config, section, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('section')
  const showElement = filterElement(filter, section)

  const fetchEdit = () => elementActions.fetchElement('sections', section.id)
  const fetchCopy = () => elementActions.fetchElement('sections', section.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('sections', section.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('sections', {...section, locked: !section.locked })

  const createPage = () => elementActions.createElement('pages', { section })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <NestedLink element={section} verboseName={verboseName} onClick={fetchNested} />
        <EditLink verboseName={verboseName} onClick={fetchEdit} />
        <CopyLink verboseName={verboseName} onClick={fetchCopy} />
        <AddLink element={section} verboseName={gettext('page')} onClick={createPage} />
        <LockedLink element={section} verboseName={verboseName} onClick={toggleLocked} />
        <ExportLink element={section} elementType="sections" verboseName={verboseName}
                    exportFormats={config.settings.export_formats} />
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
