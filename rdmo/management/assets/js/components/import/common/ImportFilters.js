import React from 'react'
import PropTypes from 'prop-types'
import {FilterString, FilterUriPrefix} from '../../common/Filter'
import get from 'lodash/get'
import {getUriPrefixes} from '../../../utils/filter'
import {Checkbox} from '../../common/Checkboxes'

const ImportFilters = ({ config, elements, updatedAndChanged, filteredElements, configActions }) => {
  console.log('importFilter', updatedAndChanged, elements)
  const updateFilterString = (value) => configActions.updateConfig('filter.import.elements.search', value)
  const getValueFilterString = () => get(config, 'filter.import.elements.search', '')
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.import.elements.uri_prefix', value)
  const getValueFilterUirPrefix = () => get(config, 'filter.import.elements.uri_prefix', '')
  const updateFilterChanged = (value) => configActions.updateConfig('filter.import.elements.changed', value)
  const getValueFilterChanged = () => get(config, 'filter.import.elements.changed', false)

  return (
    <div className="panel-body">
    <div className="row">
      <div className="row">
        <div className={'col-sm-8'}>
          <FilterString value={getValueFilterString()} onChange={updateFilterString}
                        placeholder={gettext('Filter uri')}/>
        </div>
        <div className="col-sm-4">
          <FilterUriPrefix value={getValueFilterUirPrefix()}
                           onChange={updateFilterUriPrefix}
                           options={getUriPrefixes(elements)}/>
        </div>
      </div>
      <div className="row-checkbox">
        {
          updatedAndChanged.length > 0 &&
          <div className="pull-left">
            <div className="checkboxes">
              <span className="mr-10">{gettext('Changed:')}</span>
              <Checkbox label={<code
                className="code-questions">{gettext('Filter changed')}{' ('}{updatedAndChanged.length}{') '}</code>}
                        value={getValueFilterChanged()} onChange={updateFilterChanged}/>
            </div>
          </div>
        }
        { filteredElements.length > 0 &&
          <div className="pull-right">
            <span>{gettext('Shown')}: {filteredElements.length} / {elements.length} </span>
          </div>
        }


      </div>
    </div>
    </div>
  )
}

ImportFilters.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  updatedAndChanged: PropTypes.array.isRequired,
  filteredElements: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
}

export default ImportFilters
