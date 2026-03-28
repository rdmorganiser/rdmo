import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { createElement, fetchElement, storeElement } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import { AddLink, CodeLink, CopyLink, EditLink, ExportLink, LockedLink, NestedLink } from '../common/Links'

const Attribute = ({ attribute, display = 'list', indent = 0, filter = null, filterEditors = false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, attribute)

  const editUrl = buildPath('attributes', attribute.id)
  const copyUrl = buildPath('attributes', attribute.id, 'copy')
  const nestedUrl = buildPath('attributes', attribute.id, 'nested')
  const exportUrl = buildApiPath('domain', 'attributes', attribute.id, 'export')

  const fetchEdit = () => dispatch(fetchElement('attributes', attribute.id))
  const fetchCopy = () => dispatch(fetchElement('attributes', attribute.id, 'copy'))
  const fetchNested = () => dispatch(fetchElement('attributes', attribute.id, 'nested'))
  const toggleLocked = () => dispatch(storeElement('attributes', {...attribute, locked: !attribute.locked }))

  const createAttribute = () => dispatch(createElement('attributes', { attribute }))

  const elementNode = (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex align-items-center gap-2">
        <strong>{gettext('Attribute')}{':'}</strong>
        <CodeLink className="flex-grow-1" type="domain" uri={attribute.uri} href={editUrl}
          onClick={() => fetchEdit()} />

        <div className="d-flex align-items-center gap-1">
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
      </div>
      <ElementErrors element={attribute} />
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          {elementNode}
        </li>
      )
    case 'nested':
      return (
        <>
          {
            <div className="card mt-2" style={{ marginLeft: `calc(${indent} * var(--rdmo-management-indent))` }}>
              <div className="card-body">
                {elementNode}
              </div>
            </div>
          }
          {
            attribute.elements.map((attribute, index) => (
              <Attribute key={index} attribute={attribute} display="nested" filter={filter} indent={indent + 1} />
            ))
          }
        </>
      )
    case 'plain':
      return elementNode
  }
}

Attribute.propTypes = {
  attribute: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool
}

export default Attribute
