import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import QuestionSet from './QuestionSet'
import Question from './Question'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink,
         ExportLink, CodeLink } from '../common/Links'
import { Drag, Drop } from '../common/DragAndDrop'

const Page = ({ config, page, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('page')
  const showElement = filterElement(filter, page)

  const fetchEdit = () => elementActions.fetchElement('pages', page.id)
  const fetchCopy = () => elementActions.fetchElement('pages', page.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('pages', page.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('pages', {...page, locked: !page.locked })

  const createQuestionSet = () => elementActions.createElement('questionsets', { page })
  const createQuestion = () => elementActions.createElement('questions', { page })

  const fetchAttribute = () => elementActions.fetchElement('attributes', page.attribute)

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <NestedLink element={page} verboseName={verboseName} onClick={fetchNested} />
        <EditLink verboseName={verboseName} onClick={fetchEdit} />
        <CopyLink verboseName={verboseName} onClick={fetchCopy} />
        <AddLink element={page} verboseName={gettext('question')} verboseNameAlt={gettext('question set')}
                 onClick={createQuestion} onAltClick={createQuestionSet} />
        <LockedLink element={page} verboseName={verboseName} onClick={toggleLocked} />
        <ExportLink element={page} elementType="pages" verboseName={verboseName}
                    exportFormats={config.settings.export_formats} />
        {display == 'nested' && <Drag element={page} />}
      </div>
      <div>
        <p>
          <strong>{gettext('Page')}{': '}</strong> {page.title}
        </p>
        {
          config.display.uri.pages && <p>
            <CodeLink className="code-questions" uri={page.uri} onClick={() => fetchEdit()} />
          </p>
        }
        {
          config.display.uri.attributes && page.attribute_uri && <p>
            <CodeLink className="code-domain" uri={page.attribute_uri} onClick={() => fetchAttribute()} />
          </p>
        }
        <ElementErrors element={page} />
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
            showElement && config.display.elements.pages && (
              <Drop element={page} elementActions={elementActions}>
                <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
                  <div className="panel-heading">
                    { elementNode }
                  </div>
                </div>
              </Drop>
            )
          }
          {
            page.elements.map((element, index) => {
              if (element.model == 'questions.questionset') {
                return <QuestionSet key={index} config={config} questionset={element} elementActions={elementActions}
                                    display="nested" filter={filter}  indent={indent + 1} />
              } else {
                return <Question key={index} config={config} question={element} elementActions={elementActions}
                                 display="nested" filter={filter}  indent={indent + 1}  />
              }
            })
          }
          <Drop element={page} elementActions={elementActions} indent={indent} mode="after" />
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
