import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement, storeElement } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import { CodeLink, CopyLink, EditLink, ExportLink, LockedLink } from '../common/Links'

const Option = ({ option, display='list', indent=0, filter=false, filterEditors=false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, option)

  const editUrl = buildPath('options', option.id)
  const copyUrl = buildPath('options', option.id, 'copy')
  const exportUrl = buildApiPath('options', 'options', option.id, 'export')

  const fetchEdit = () => dispatch(fetchElement('options', option.id))
  const fetchCopy = () => dispatch(fetchElement('options', option.id, 'copy'))
  const toggleLocked = () => dispatch(storeElement('options', {...option, locked: !option.locked }))

  const displayUriOptions = isTruthy(get(config, 'display.uri.options', true))

  const elementNode = (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex align-items-center gap-2">
        <strong>{gettext('Option')}{':'}</strong>
        <div className="flex-grow-1">
          <Html html={option.text} />
        </div>

        <div className="d-flex align-items-center gap-1">
          <ReadOnlyIcon title={gettext('This option is read only')} show={option.read_only} />
          <EditLink title={gettext('Edit option')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy option')} href={copyUrl} onClick={fetchCopy} />
          <LockedLink title={option.locked ? gettext('Unlock option') : gettext('Lock option')}
            locked={option.locked} onClick={toggleLocked} disabled={option.read_only} />
          <ExportLink title={gettext('Export option')} exportUrl={exportUrl}
            exportFormats={config.settings.export_formats} />
        </div>
      </div>
      {
        displayUriOptions &&
        <CodeLink type="options" uri={option.uri} href={editUrl} onClick={() => fetchEdit()} />
      }
      <ElementErrors element={option} />
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          { elementNode }
        </li>
      )
    case 'nested':
      return showElement && (
        <div className="card mt-2" style={{ marginLeft: `calc(${indent} * var(--rdmo-management-indent))` }}>
          <div className="card-body">
            { elementNode }
          </div>
        </div>
      )
  }
}

Option.propTypes = {
  option: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool
}

export default Option
