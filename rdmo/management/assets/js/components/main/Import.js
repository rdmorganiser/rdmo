import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import isEmpty from 'lodash/isEmpty'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'
import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'

import ImportElement from '../import/ImportElement'

import { codeClass, verboseNames } from '../../constants/elements'

const Import = ({ config, imports, importActions }) => {
  const { elements, success } = imports
  const updateFilterString = (value) => importActions.updateConfig('filter.import.elements.search', value)
  const updateFilterUriPrefix = (value) => importActions.updateConfig('filter.import.elements.uri_prefix', value)
  const updateDisplayCatalogURI = (value) => importActions.updateConfig('display.uri.catalogs', value)
  const updatedElements = elements.filter(element => element.updated)
  const createdElements = elements.filter(element => element.created)
  const importErrors = elements.filter(element => !isEmpty(element.errors))

  return (
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')}</strong>
        <div className="pull-right">
          {
            updatedElements.length > -1 && <span>{gettext('Updated')}: {updatedElements.length} </span>
          }
          {
            createdElements.length > -1 && <span>{gettext('Created')}: {createdElements.length} </span>
          }
          {
            importErrors.length > -1 && <span>{gettext('Errors')}: {importErrors.length} </span>
          }
        </div>
      </div>
    <div className="panel-body">
    {/* TODO: still to implement functions for filter, uri_prefix dropdown, disply checkox etc.. */}
    <div className="row">
      <div className={'col-sm-8'}>
        <FilterString value={get(config, 'filter.catalogs.search', '')} onChange={updateFilterString}
                      placeholder={gettext('Filter uri')} />
      </div>
      <div className="col-sm-4">
        <FilterUriPrefix value={get(config, 'filter.catalogs.uri_prefix', '')} onChange={updateFilterUriPrefix}
                        options={getUriPrefixes(elements)} />
      </div>

    </div>
    <div className="checkboxes">
      <span className="mr-10">{gettext('Show URIs:')}</span>
      <Checkbox label={<code className="code-questions">{gettext('Catalogs')}</code>}
                value={get(config, 'display.uri.catalogs', true)} onChange={updateDisplayCatalogURI} />
    </div>
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
              return <ImportElement key={index} config={config} instance={element} importActions={importActions} />
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
