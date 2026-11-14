import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
import OptionSet from '../element/OptionSet'

const OptionSets = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const optionsets = useSelector((state) => state.elements.optionsets)

  const [filterString, setFilterString] = useConfig('filter.optionsets.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.optionsets.uri_prefix', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const createOptionSet = () => dispatch(createElement('optionsets'))

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Option sets')}</strong>
          <BackButton />
          <NewButton onClick={createOptionSet} />
        </div>
      </div>

      <div className="card-body">
        <div className="row">
          <div className={settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString
              value={filterString} onChange={setFilterString}
              label={gettext('Filter option sets')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix
              value={filterUriPrefix} onChange={setFilterUriPrefix}
              options={getUriPrefixes(optionsets)} />
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

      {
        !isEmpty(optionsets) && (
          <ul className="list-group list-group-flush border-top">
            {
              optionsets.map((optionset, index) => (
                <OptionSet
                  key={index} optionset={optionset}
                  filter="optionsets" filterEditors={true} />
              ))
            }
          </ul>
        )
      }
    </div>
  )
}

export default OptionSets
