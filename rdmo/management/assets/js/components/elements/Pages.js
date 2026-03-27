import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
import Page from '../element/Page'

const Pages = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const pages = useSelector((state) => state.elements.pages)

  const updateFilterString = (value) => dispatch(updateConfig('filter.pages.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.pages.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriPages = isTruthy(get(config, 'display.uri.pages', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))

  const toggleDisplayUriPages = () => dispatch(updateConfig('display.uri.pages', !displayUriPages))
  const toggleDisplayUriAttributes = () => dispatch(updateConfig('display.uri.attributes', !displayUriAttributes))
  const toggleDisplayUriConditions = () => dispatch(updateConfig('display.uri.conditions', !displayUriConditions))

  const createPage = () => dispatch(createElement('pages'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Pages')}</strong>
          <BackButton />
          <NewButton onClick={createPage} />
        </div>
      </div>

      <div className="card-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.pages.search', '')} onChange={updateFilterString}
              label={gettext('Filter pages')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.pages.uri_prefix', '')} onChange={updateFilterUriPrefix}
              options={getUriPrefixes(pages)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
            </div>
          }
        </div>
        <div className="input-group input-group-sm mb-2">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={toggleDisplayUriPages} className={btnClass(displayUriPages)}>
            {gettext('Pages')}
          </button>
          <button type="button" onClick={toggleDisplayUriAttributes} className={btnClass(displayUriAttributes)}>
            {gettext('Attributes')}
          </button>
          <button type="button" onClick={toggleDisplayUriConditions} className={btnClass(displayUriConditions)}>
            {gettext('Conditions')}
          </button>
        </div>
      </div>

      {
        !isEmpty(pages) && (
          <ul className="list-group list-group-flush">
            {
              pages.map((page, index) => (
                <Page key={index} config={config} page={page}
                  filter="pages" filterEditors={true} />
              ))
            }
          </ul>

        )
      }
    </div>
  )
}

export default Pages
