import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElements } from '../../utils/filter'

import QuestionSet from './QuestionSet'
import Question from './Question'
import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Page = ({ config, page, fetchElement, storeElement, list=true, indent=0 }) => {

  const verboseName = gettext('page')

  const fetchEdit = () => fetchElement('pages', page.id)
  const fetchNested = () => fetchElement('pages', page.id, 'nested')
  const toggleLocked = () => storeElement('pages', {...page, locked: !page.locked })

  const elementNode = (
    <div className="element">
      <div className="element-options">
        <EditLink element={page} verboseName={verboseName} onClick={fetchEdit} />
        <LockedLink element={page} verboseName={verboseName} onClick={toggleLocked} />
        <NestedLink element={page} verboseName={verboseName} onClick={fetchNested} />
        <ExportLink element={page} verboseName={verboseName} />
      </div>
      <div style={{ paddingLeft: 15 * indent }}>
        <p>
          <strong>{gettext('Page')}{': '}</strong> {page.title}
        </p>
        <p>
          <code className="code-questions">{page.uri}</code>
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
          filterElements(config, page.elements).map((element, index) => {
            if (isUndefined(element.text)) {
              return <QuestionSet key={index} config={config} questionset={element}
                                  fetchElement={fetchElement} storeElement={storeElement}
                                  indent={indent + 1} />
            } else {
              return <Question key={index} config={config} question={element}
                               fetchElement={fetchElement} storeElement={storeElement}
                               indent={indent + 1} />
            }
          })
        }
      </React.Fragment>
    )
  } else {
    return elementNode
  }
}

Page.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired,
  list: PropTypes.bool,
  indent: PropTypes.number
}

export default Page
