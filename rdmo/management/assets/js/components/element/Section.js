import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElements } from '../../utils/filter'

import Page from './Page'
import { EditLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Section = ({ config, section, elementActions, list=true }) => {

  const verboseName = gettext('section')

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
        <p>
          <code className="code-questions">{section.uri}</code>
        </p>
      </div>
    </div>
  )

  if (list) {
    return (
      <React.Fragment>
        <li className="list-group-item">
          { elementNode }
        </li>
        {
          filterElements(config, section.elements).map((page, index) => (
            <Page key={index} config={config} page={page}
                  elementActions={elementActions} indent={1} />
          ))
        }
      </React.Fragment>
    )
  } else {
    return elementNode
  }
}

Section.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  list: PropTypes.bool
}

export default Section
