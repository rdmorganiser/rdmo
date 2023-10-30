import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import Page from './Page'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink, ExportLink,
         CodeLink, ShowElementsLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'
import { Drag, Drop } from '../common/DragAndDrop'


const Section = ({ config, section, configActions, elementActions, display='list', indent=0,
                   filter=false, filterEditors=false, order }) => {

  const showElement = filterElement(config, filter, false, filterEditors, section)
  const showElements = get(config, `display.elements.sections.${section.id}`, true)

  const editUrl = buildPath(config.baseUrl, 'sections', section.id)
  const copyUrl = buildPath(config.baseUrl, 'sections', section.id, 'copy')
  const nestedUrl = buildPath(config.baseUrl, 'sections', section.id, 'nested')
  const exportUrl = buildPath('/api/v1/', 'questions', 'sections', section.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('sections', section.id)
  const fetchCopy = () => elementActions.fetchElement('sections', section.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('sections', section.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('sections', {...section, locked: !section.locked })
  const toggleElements = () => configActions.toggleElements(section)

  const createPage = () => elementActions.createElement('pages', { section })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This section is read only')} show={section.read_only} />
        <NestedLink title={gettext('View section nested')} href={nestedUrl} onClick={fetchNested} show={display != 'nested'} />
        <ShowElementsLink showElements={showElements} show={display == 'nested'} onClick={toggleElements} />
        <EditLink title={gettext('Edit section')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy section')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add page')} onClick={createPage} disabled={section.read_only} />
        <LockedLink title={section.locked ? gettext('Unlock section')
                                          : gettext('Lock section')}
                    locked={section.locked} onClick={toggleLocked} disabled={section.read_only} />
        <ExportLink title={gettext('Export section')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
        <Drag element={section} show={display == 'nested'} />
      </div>
      <div>
        <p>
          <strong>{gettext('Section')}{': '}</strong> {section.title}
        </p>
        {
          get(config, 'display.uri.sections', true) &&
          <CodeLink className="code-questions" uri={section.uri} onClick={() => fetchEdit()} order={order} />
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
            showElement && (
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
            showElements && section.elements.map((page, index) => {
              const pageInfo = section.pages.find(info => info.page === page.id)
              const pageOrder = pageInfo ? pageInfo.order : undefined

              return (
                <Page
                  key={index}
                  config={config}
                  page={page}
                  configActions={configActions}
                  elementActions={elementActions}
                  display="nested"
                  filter={filter}
                  indent={indent + 1}
                  order={pageOrder}
                />
              )
            })
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
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default Section
