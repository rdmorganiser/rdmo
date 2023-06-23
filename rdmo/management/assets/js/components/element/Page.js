import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import QuestionSet from './QuestionSet'
import Question from './Question'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink,
         ExportLink, CodeLink } from '../common/Links'
import { Drag, Drop } from '../common/DragAndDrop'

const Page = ({ config, page, elementActions, display='list', filter=null, indent=0 }) => {

  const showElement = filterElement(filter, page)

  const editUrl = buildPath(config.baseUrl, 'pages', page.id)
  const copyUrl = buildPath(config.baseUrl, 'pages', page.id, 'copy')
  const nestedUrl = buildPath(config.baseUrl, 'pages', page.id, 'nested')
  const exportUrl = buildPath('/api/v1/', 'questions', 'pages', page.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('pages', page.id)
  const fetchCopy = () => elementActions.fetchElement('pages', page.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('pages', page.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('pages', {...page, locked: !page.locked })

  const createQuestionSet = () => elementActions.createElement('questionsets', { page })
  const createQuestion = () => elementActions.createElement('questions', { page })

  const fetchAttribute = () => elementActions.fetchElement('attributes', page.attribute)
  const fetchCondition = (index) => elementActions.fetchElement('conditions', page.conditions[index])

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <NestedLink title={gettext('View page nested')} href={nestedUrl} onClick={fetchNested} />
        <EditLink title={gettext('Edit page')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy page')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add question')} altTitle={gettext('Add question set')}
                 onClick={createQuestion} onAltClick={createQuestionSet} />
        <LockedLink title={page.locked ? gettext('Unlock page') : gettext('Lock page')}
                    locked={page.locked} onClick={toggleLocked} />
        <ExportLink title={gettext('Export page')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
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
        {
          config.display.uri.conditions && page.condition_uris.map((uri, index) => (
            <p key={index}>
              <CodeLink className="code-conditions" uri={uri} onClick={() => fetchCondition(index)} />
            </p>
          ))
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
