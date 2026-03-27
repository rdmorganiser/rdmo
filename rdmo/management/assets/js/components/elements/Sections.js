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
import Section from '../element/Section'

const Sections = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const sections = useSelector((state) => state.elements.sections)

  const updateFilterString = (value) => dispatch(updateConfig('filter.sections.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.sections.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriSections = isTruthy(get(config, 'display.uri.sections', true))

  const toggleDisplayUriSections = () => dispatch(updateConfig('display.uri.sections', !displayUriSections))

  const createSection = () => dispatch(createElement('sections'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Sections')}</strong>
          <BackButton />
          <NewButton onClick={createSection} />
        </div>
      </div>

      <div className="card-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.sections.search', '')} onChange={updateFilterString}
              label={gettext('Filter sections')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.sections.uri_prefix', '')} onChange={updateFilterUriPrefix}
              options={getUriPrefixes(sections)} />
          </div>
          {
            config.settings.multisite && (
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                  options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
              </div>
            )
          }
        </div>
        <div className="input-group input-group-sm">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={toggleDisplayUriSections} className={btnClass(displayUriSections)}>
            {gettext('Sections')}
          </button>
        </div>
      </div>

      {
        !isEmpty(sections) && (
          <ul className="list-group list-group-flush">
            {
              sections.map((section, index) => (
                <Section key={index} config={config} section={section}
                  filter="sections" filterEditors={true} />
              ))
            }
          </ul>
        )
      }
    </div>
  )
}

export default Sections
