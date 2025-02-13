import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink, ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Attribute = ({ config, attribute, elementActions, display='list', indent=0,
                     filter=null, filterEditors=false }) => {

  const showElement = filterElement(config, filter, false, filterEditors, attribute)

  const editUrl = buildPath('attributes', attribute.id)
  const copyUrl = buildPath('attributes', attribute.id, 'copy')
  const nestedUrl = buildPath('attributes', attribute.id, 'nested')
  const exportUrl = buildApiPath('domain', 'attributes', attribute.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('attributes', attribute.id)
  const fetchCopy = () => elementActions.fetchElement('attributes', attribute.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('attributes', attribute.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('attributes', {...attribute, locked: !attribute.locked })

  const createAttribute = () => elementActions.createElement('attributes', { attribute })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This attribute is read only')} show={attribute.read_only} />
        <NestedLink title={gettext('View attribute nested')} href={nestedUrl} onClick={fetchNested}
                    show={!attribute.is_leaf_node} />
        <EditLink title={gettext('Edit attribute')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy attribute')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add attribute')} onClick={createAttribute} disabled={attribute.read_only} />
        <LockedLink title={attribute.locked ? gettext('Unlock attribute') : gettext('Lock attribute')}
                    locked={attribute.locked} onClick={toggleLocked} disabled={attribute.read_only} />
        <ExportLink title={gettext('Export attribute')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} csv={true} />
      </div>
      <div>
        <p>
          <strong>{gettext('Attribute')}{': '}</strong>
          <CodeLink className="code-domain" uri={attribute.uri} href={editUrl} onClick={() => fetchEdit()} />
        </p>
        <ElementErrors element={attribute} />
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
      return (
        <>
          {
            showElement && <div className="panel panel-default" style={{ marginLeft: 30 * indent }}>
              <div className="panel-body">
                { elementNode }
              </div>
            </div>
          }
          {
            attribute.elements.map((attribute, index) => (
              <Attribute key={index} config={config} attribute={attribute} elementActions={elementActions}
                         display="nested" filter={filter} indent={indent + 1} />
            ))
          }
        </>
      )
    case 'plain':
      return elementNode
  }
}

Attribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool
}

export default Attribute
