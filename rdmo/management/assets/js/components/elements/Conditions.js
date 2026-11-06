import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix} from '../common/Filter'
import Condition from '../element/Condition'

const Conditions = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const conditions = useSelector((state) => state.elements.conditions)

  const [filterString, setFilterString] = useConfig('filter.conditions.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.conditions.uri_prefix', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const createCondition = () => dispatch(createElement('conditions'))

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Conditions')}</strong>
          <BackButton />
          <NewButton onClick={createCondition} />
        </div>
      </div>

      <div className="card-body">
        <div className="row">
          <div className={settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString
              value={filterString} onChange={setFilterString}
              label={gettext('Filter conditions')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix
              value={filterUriPrefix} onChange={setFilterUriPrefix}
              options={getUriPrefixes(conditions)} />
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
        !isEmpty(conditions) && (
          <ul className="list-group list-group-flush border-top">
            {
              conditions.map((condition, index) => (
                <Condition
                  key={index} condition={condition}
                  filter="conditions" filterEditors={true} />
              ))
            }
          </ul>
        )
      }
    </div>
  )
}

export default Conditions
