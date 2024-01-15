import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'
import { FilterString, FilterUriPrefix } from '../common/Filter'

import ImportElement from '../import/ImportElement'
import ImportSuccesElement from '../import/ImportSuccessElement'

const Import = ({ config, imports, importActions }) => {
  const { filename, elements, success } = imports
  const updateFilterString = (value) => importActions.updateConfig('filter.import.elements.search', value)
  const updateFilterUriPrefix = (value) => importActions.updateConfig('filter.import.elements.uri_prefix', value)
  const updatedElements = elements.filter(element => element.updated)
  const createdElements = elements.filter(element => element.created)
  const updatedAndChangedElements = elements.filter(element => element.updated && !isEmpty(element.updated_and_changed))
  const updatedAndSameElements = elements.filter(element => element.updated && isEmpty(element.updated_and_changed))
  const importErrors = elements.filter(element => !isEmpty(element.errors))


  return (
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')} from file {filename}</strong>
        <div className="pull-right">
          {
            elements.length > -1 && <span>{gettext('Total')}: {elements.length} </span>
          }
          {
            updatedElements.length > -1 && <span> {gettext('Updated')}: {updatedElements.length}
            {' ('}{gettext('Changed')}: {updatedAndChangedElements.length}
            {' '}{gettext('Same')}: {updatedAndSameElements.length}{') '}
              </span>
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
    {/* TODO: still to implement functions for filter, uri_prefix dropdown. */}
    <div className="row">
      <div className={'col-sm-8'}>
        <FilterString value={get(config, 'filter.import.elements.search', '')} onChange={updateFilterString}
                      placeholder={gettext('Filter uri')} />
      </div>
      <div className="col-sm-4">
      {/* TODO: add update of the filter to elements */}
        <FilterUriPrefix value={get(config, 'filter.import.elements.uri_prefix', '')} onChange={updateFilterUriPrefix}
                        options={getUriPrefixes(elements)} />
      </div>

    </div>
    </div>
      <ul className="list-group">
      {
        elements.map((element, index) => {
          if (success) {
            return <ImportSuccesElement key={index} instance={element}/>
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
