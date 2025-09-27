import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { fetchElement, storeElement, createElement } from '../../actions/elementActions'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink,
         ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const OptionSet = ({ optionset, display='list', filter=false, filterEditors=false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, optionset)

  const editUrl = buildPath('optionsets', optionset.id)
  const copyUrl = buildPath('optionsets', optionset.id, 'copy')
  const nestedUrl = buildPath('optionsets', optionset.id, 'nested')
  const exportUrl = buildApiPath('options', 'optionsets', optionset.id, 'export')

  const getConditionUrl = (index) => buildPath(config.apiUrl, 'conditions', 'conditions', optionset.conditions[index])

  const fetchEdit = () => dispatch(fetchElement('optionsets', optionset.id))
  const fetchCopy = () => dispatch(fetchElement('optionsets', optionset.id, 'copy'))
  const fetchNested = () => dispatch(fetchElement('optionsets', optionset.id, 'nested'))
  const toggleLocked = () => dispatch(storeElement('optionsets', {...optionset, locked: !optionset.locked }))

  const createOption = () => dispatch(createElement('options', { optionset }))
  const fetchCondition = (index) => dispatch(fetchElement('conditions', optionset.conditions[index]))

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This option set is read only')} show={optionset.read_only} />
        <NestedLink title={gettext('View option set nested')} href={nestedUrl} onClick={fetchNested} />
        <EditLink title={gettext('Edit option set')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy option set')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add option')} onClick={createOption} disabled={optionset.read_only} />
        <LockedLink title={optionset.locked ? gettext('Unlock option set') : gettext('Lock option set')}
                    locked={optionset.locked} onClick={toggleLocked} disabled={optionset.read_only} />
        <ExportLink title={gettext('Export option set')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
      </div>
      <div>
        <p>
          <strong>{gettext('Option set')}{':'}</strong>
          <CodeLink className="code-options" uri={optionset.uri} href={editUrl} onClick={() => fetchEdit()} />
        </p>
        {
          get(config, 'display.uri.conditions', true) && optionset.condition_uris.map((uri, index) => (
            <p key={index}>
              <CodeLink
                className="code-conditions"
                uri={uri}
                href={getConditionUrl(index)}
                onClick={() => fetchCondition(index)}
              />
            </p>
          ))
        }
        <ElementErrors element={optionset} />
      </div>
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          { elementNode }
        </li>
      )
    case 'plain':
      return elementNode
  }
}

OptionSet.propTypes = {
  optionset: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool
}

export default OptionSet
