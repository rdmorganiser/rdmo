import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Option from '../element/Option'

const Options = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const options = useSelector((state) => state.elements.options)

  const updateFilterString = (value) => dispatch(updateConfig('filter.options.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.options.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriOptions = isTruthy(get(config, 'display.uri.options', true))

  const toggleDisplayUriOptions = () => dispatch(updateConfig('display.uri.options', !displayUriOptions))

  const createOption = () => dispatch(createElement('options'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Options')}</strong>
          <BackButton />
          <NewButton onClick={createOption} />
        </div>
      </div>

      <div className="card-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.options.search', '')} onChange={updateFilterString}
                          label={gettext('Filter options')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.options.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(options)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
            </div>
          }
        </div>
        <div className="input-group input-group-sm">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={toggleDisplayUriOptions} className={btnClass(displayUriOptions)}>
            {gettext('Options')}
          </button>
        </div>
      </div>

      {
        !isEmpty(options) && (
          <ul className="list-group list-group-flush">
          {
            options.map((option, index) => (
              <Option key={index} config={config} option={option}
                      filter="options" filterEditors={true} />
            ))
          }
          </ul>
        )
      }
    </div>
  )
}

export default Options
