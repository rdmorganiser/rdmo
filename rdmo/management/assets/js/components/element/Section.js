import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isNil from 'lodash/isNil'

import { filterElement } from '../../utils/filter'

import Page from './Page'
import { EditLink, LockedLink, NestedLink, ExportLink } from '../common/Links'

const Section = ({ config, section, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('section')
  const showElement = filterElement(filter, section) && config.display.elements.sections

  const fetchEdit = () => elementActions.fetchElement('sections', section.id)
  const fetchNested = () => elementActions.fetchElement('sections', section.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('sections', {...section, locked: !section.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={section} verboseName={verboseName} onClick={fetchEdit} />
        <LockedLink element={section} verboseName={verboseName} onClick={toggleLocked} />
        <NestedLink element={section} verboseName={verboseName} onClick={fetchNested} />
        <ExportLink element={section} verboseName={verboseName} />
      </div>
      <div>
        <p>
          <strong>{gettext('Section')}{': '}</strong> {section.title}
        </p>
        {
          config.display.uri.sections && <p>
            <code className="code-questions">{section.uri}</code>
          </p>
        }
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
            showElement && <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
              <div className="panel-heading">
                { elementNode }
              </div>
            </div>
          }
          {
            section.elements.map((page, index) => (
              <Page key={index} config={config} page={page} elementActions={elementActions}
                    display="nested" filter={filter} indent={indent + 1} />
            ))
          }
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
