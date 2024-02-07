import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import isEmpty from 'lodash/isEmpty'

import ImportAttribute from '../import/ImportAttribute'
import ImportCatalog from '../import/ImportCatalog'
import ImportCondition from '../import/ImportCondition'
import ImportOption from '../import/ImportOption'
import ImportOptionSet from '../import/ImportOptionSet'
import ImportPage from '../import/ImportPage'
import ImportQuestion from '../import/ImportQuestion'
import ImportQuestionSet from '../import/ImportQuestionSet'
import ImportSection from '../import/ImportSection'
import ImportTask from '../import/ImportTask'
import ImportView from '../import/ImportView'

import { codeClass, verboseNames } from '../../constants/elements'

const Import = ({ config, imports, importActions }) => {
  const { elements, success } = imports

  return (
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')}</strong>
      </div>

      <ul className="list-group">
      {
        elements.map((element, index) => {
          if (success) {
            return (
              <li key={index} className="list-group-item">
                <p>
                  <strong>{verboseNames[element.model]}{' '}</strong>
                  <code className={codeClass[element.model]}>{element.uri}</code>
                  {element.created && <span className="text-success">{' '}{gettext('created')}</span>}
                  {element.updated && <span className="text-info">{' '}{gettext('updated')}</span>}
                  {
                    !isEmpty(element.errors) && !(element.created || element.updated) &&
                    <span className="text-danger">{' '}{gettext('could not be imported')}</span>
                  }
                  {
                    !isEmpty(element.errors) && (element.created || element.updated) &&
                    <>{', '}<span className="text-danger">{gettext('but could not be added to parent element')}</span></>
                  }
                  {'.'}
                </p>
                {element.warnings.map(message => <p key={uniqueId()} className="text-warning">{message}</p>)}
                {element.errors.map(message => <p key={uniqueId()} className="text-danger">{message}</p>)}
              </li>
            )
          } else {
            switch (element.model) {
              case 'questions.catalog':
                return <ImportCatalog key={index} config={config} catalog={element} importActions={importActions} />
              case 'questions.section':
                return <ImportSection key={index} config={config} section={element} importActions={importActions} />
              case 'questions.page':
                return <ImportPage key={index} config={config} page={element} importActions={importActions} />
              case 'questions.questionset':
                return <ImportQuestionSet key={index} config={config} questionset={element} importActions={importActions} />
              case 'questions.question':
                return <ImportQuestion key={index} config={config} question={element} importActions={importActions} />
              case 'domain.attribute':
                return <ImportAttribute key={index} config={config} attribute={element} importActions={importActions} />
              case 'options.optionset':
                return <ImportOptionSet key={index} config={config} optionset={element} importActions={importActions} />
              case 'options.option':
                return <ImportOption key={index} config={config} option={element} importActions={importActions} />
              case 'conditions.condition':
                return <ImportCondition key={index} config={config} condition={element} importActions={importActions} />
              case 'tasks.task':
                return <ImportTask key={index} config={config} task={element} importActions={importActions} />
              case 'views.view':
                return <ImportView key={index} config={config} view={element} importActions={importActions} />
              default:
                return null
            }
          }
        })
      }
      </ul>
    </div>
  )
}

Import.propTypes = {
  config: PropTypes.object.isRequired,
  imports: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default Import
