import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { createElement, fetchElement, storeElement } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import { AddLink, CodeLink, CopyLink, EditLink,          ExportLink, LockedLink, NestedLink } from '../common/Links'

const OptionSet = ({ optionset, display = 'list', filter = false, filterEditors = false }) => {
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

  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))

  const elementNode = (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex align-items-center gap-2">
        <strong>{gettext('Option set')}{':'}</strong>
        <CodeLink className="flex-grow-1" type="options" uri={optionset.uri} href={editUrl}
          onClick={() => fetchEdit()} />

        <div className="d-flex align-items-center gap-1">
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
      </div>
      {
        displayUriConditions && optionset.condition_uris.map((uri, index) => (
          <CodeLink
            key={index}
            type="conditions"
            uri={uri}
            href={getConditionUrl(index)}
            onClick={() => fetchCondition(index)}
          />
        ))
      }
      <ElementErrors element={optionset} />
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          {elementNode}
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
