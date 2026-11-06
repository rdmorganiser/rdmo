import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
import Page from '../element/Page'

const Pages = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const pages = useSelector((state) => state.elements.pages)

  const [filterString, setFilterString] = useConfig('filter.pages.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.pages.uri_prefix', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const [displayUriPages, setDisplayUriPages] = useConfig('display.uri.pages', true)
  const [displayUriAttributes, setDisplayUriAttributes] = useConfig('display.uri.attributes', true)
  const [displayUriConditions, setDisplayUriConditions] = useConfig('display.uri.conditions', true)

  const toggleDisplayUriPages = () => setDisplayUriPages(!displayUriPages)
  const toggleDisplayUriAttributes = () => setDisplayUriAttributes(!displayUriAttributes)
  const toggleDisplayUriConditions = () => setDisplayUriConditions(!displayUriConditions)

  const createPage = () => dispatch(createElement('pages'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Pages')}</strong>
          <BackButton />
          <NewButton onClick={createPage} />
        </div>
      </div>

      <div className="card-body">
        <div className="mb-lg-2">
          <div className="row">
            <div className={settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
              <FilterString
                value={filterString} onChange={setFilterString}
                label={gettext('Filter pages')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix
                value={filterUriPrefix} onChange={setFilterUriPrefix}
                options={getUriPrefixes(pages)} />
            </div>
            {
              settings.multisite && (
                <div className="col-sm-2">
                  <FilterSite
                    value={filterEditor} onChange={setFilterEditor}
                    options={sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
                </div>
              )
            }
          </div>
        </div>
        <div className="input-group input-group-sm row-gap-1">
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
          <ul className="list-group list-group-flush border-top">
            {
              pages.map((page, index) => (
                <Page
                  key={index} page={page}
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
