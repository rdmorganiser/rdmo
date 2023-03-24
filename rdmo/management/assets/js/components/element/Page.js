import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElement } from '../../utils/filter'

import QuestionSet from './QuestionSet'
import Question from './Question'
import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Page = ({ config, page, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('page')
  const showElement = filterElement(filter, page)

  const fetchEdit = () => elementActions.fetchElement('pages', page.id)
  const fetchNested = () => elementActions.fetchElement('pages', page.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('pages', {...page, locked: !page.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={page} verboseName={verboseName} onClick={fetchEdit} />
        <LockedLink element={page} verboseName={verboseName} onClick={toggleLocked} />
        <NestedLink element={page} verboseName={verboseName} onClick={fetchNested} />
        <ExportLink element={page} verboseName={verboseName} />
      </div>
      <div>
        <p>
          <strong>{gettext('Page')}{': '}</strong> {page.title}
        </p>
        <p>
          <code className="code-questions">{page.uri}</code>
        </p>
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
            showElement && <div className="panel panel-default panel-nested" style={{ marginLeft: 15 * indent }}>
              <div className="panel-heading">
                { elementNode }
              </div>
            </div>
          }
          {
            page.elements.map((element, index) => {
              if (isUndefined(element.text)) {
                return <QuestionSet key={index} config={config} questionset={element} elementActions={elementActions}
                                    display="nested" filter={filter}  indent={indent + 1} />
              } else {
                return <Question key={index} config={config} question={element} elementActions={elementActions}
                                 display="nested" filter={filter}  indent={indent + 1}  />
              }
            })
          }
        </>
      )
    case 'plain':
      return elementNode
  }
}

Page.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.object,
  indent: PropTypes.number
}

export default Page
