import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, LockedLink, ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Option = ({ config, option, elementActions, display='list', indent=0, filter=false, filterEditors=false }) => {

  const showElement = filterElement(config, filter, false, filterEditors, option)

  const editUrl = buildPath('options', option.id)
  const copyUrl = buildPath('options', option.id, 'copy')
  const exportUrl = buildApiPath('options', 'options', option.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('options', option.id)
  const fetchCopy = () => elementActions.fetchElement('options', option.id, 'copy')
  const toggleLocked = () => elementActions.storeElement('options', {...option, locked: !option.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This option is read only')} show={option.read_only} />
        <EditLink title={gettext('Edit option')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy option')} href={copyUrl} onClick={fetchCopy} />
        <LockedLink title={option.locked ? gettext('Unlock option') : gettext('Lock option')}
                    locked={option.locked} onClick={toggleLocked} disabled={option.read_only} />
        <ExportLink title={gettext('Export option')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} />
      </div>
      <div>
        <p>
          <strong>{gettext('Option')}{': '}</strong>
          <span dangerouslySetInnerHTML={{ __html: option.text }}></span>
        </p>
        {
          get(config, 'display.uri.options', true) &&
          <CodeLink className="code-options" uri={option.uri} href={editUrl} onClick={() => fetchEdit()} />
        }
        <ElementErrors element={option} />
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
    case 'nested':
      return showElement && (
        <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
          <div className="panel-body">
            { elementNode }
          </div>
        </div>
      )
  }
}

Option.propTypes = {
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool
}

export default Option
