import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { useConfig, useConfigToggle } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
import Option from '../element/Option'

const Options = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const options = useSelector((state) => state.elements.options)

  const [filterString, setFilterString] = useConfig('filter.options.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.options.uri_prefix', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const [displayUriOptions, toggleDisplayUriOptions] = useConfigToggle('display.uri.options', true)


  const createOption = () => dispatch(createElement('options'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Options')}</strong>
          <BackButton />
          <NewButton onClick={createOption} />
        </div>
      </div>

      <div className="card-body">
        <div className="mb-lg-2">
          <div className="row">
            <div className={settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
              <FilterString
                value={filterString} onChange={setFilterString}
                label={gettext('Filter options')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix
                value={filterUriPrefix} onChange={setFilterUriPrefix}
                options={getUriPrefixes(options)} />
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
          <button type="button" onClick={toggleDisplayUriOptions} className={btnClass(displayUriOptions)}>
            {gettext('Options')}
          </button>
        </div>
      </div>

      {
        !isEmpty(options) && (
          <ul className="list-group list-group-flush border-top">
            {
              options.map((option, index) => (
                <Option
                  key={index} option={option}
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
