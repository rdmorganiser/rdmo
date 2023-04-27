import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'





import { ShowLink } from '../common/Links'

import Fields from './common/Fields'
import UriPrefix from './forms/UriPrefix'
import Key from './forms/Key'

import { codeClass } from '../../constants/elements'

import ImportAttribute from './ImportAttribute'
import ImportCatalog from './ImportCatalog'
import ImportCondition from './ImportCondition'
import ImportOption from './ImportOption'
import ImportOptionSet from './ImportOptionSet'
import ImportPage from './ImportPage'
import ImportQuestion from './ImportQuestion'
import ImportQuestionSet from './ImportQuestionSet'
import ImportSection from './ImportSection'
import ImportTask from './ImportTask'
import ImportView from './ImportView'

const Import = ({ config, elements, importActions }) => {
  return (
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')}</strong>
      </div>

      <ul className="list-group">
      {
        elements.map((element, index) => {
          switch (element.type) {
            case 'catalog':
              return <ImportCatalog key={index} config={config} catalog={element} importActions={importActions} />
            case 'section':
              return <ImportSection key={index} config={config} section={element} importActions={importActions} />
            case 'page':
              return <ImportPage key={index} config={config} page={element} importActions={importActions} />
            case 'questionset':
              return <ImportQuestionSet key={index} config={config} questionset={element} importActions={importActions} />
            case 'question':
              return <ImportQuestion key={index} config={config} question={element} importActions={importActions} />
            case 'attribute':
              return <ImportAttribute key={index} config={config} attribute={element} importActions={importActions} />
            case 'optionset':
              return <ImportOptionSet key={index} config={config} optionset={element} importActions={importActions} />
            case 'option':
              return <ImportOption key={index} config={config} option={element} importActions={importActions} />
            case 'condition':
              return <ImportCondition key={index} config={config} condition={element} importActions={importActions} />
            case 'task':
              return <ImportTask key={index} config={config} task={element} importActions={importActions} />
            case 'view':
              return <ImportView key={index} config={config} view={element} importActions={importActions} />
            default:
              return null
          }
        })
      }
      </ul>
    </div>
  )
}

Import.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  importActions: PropTypes.object.isRequired
}

export default Import
