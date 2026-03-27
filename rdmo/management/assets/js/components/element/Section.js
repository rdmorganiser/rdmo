import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import Html from 'rdmo/core/assets/js/components/Html'

import { createElement, dropElement, fetchElement, storeElement, toggleElements } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { Drag, Drop } from '../common/DragAndDrop'
import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import {
  AddLink,          CodeLink, CopyLink, EditLink, ExportLink,
  LockedLink, NestedLink, ShowElementsLink 
} from '../common/Links'

import Page from './Page'


const Section = ({ section, display='list', indent=0, filter=false, filterEditors=false, order }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, section)
  const showElements = isTruthy(get(config, `display.elements.sections.${section.id}`, true))

  const editUrl = buildPath('sections', section.id)
  const copyUrl = buildPath('sections', section.id, 'copy')
  const nestedUrl = buildPath('sections', section.id, 'nested')
  const exportUrl = buildApiPath('questions', 'sections', section.id, 'export')

  const fetchEdit = () => dispatch(fetchElement('sections', section.id))
  const fetchCopy = () => dispatch(fetchElement('sections', section.id, 'copy'))
  const fetchNested = () => dispatch(fetchElement('sections', section.id, 'nested'))
  const toggleLocked = () => dispatch(storeElement('sections', {...section, locked: !section.locked }))
  const toggleShowElements = () => dispatch(toggleElements(section))

  const createPage = () => dispatch(createElement('pages', { section }))

  const displayUriSections = isTruthy(get(config, 'display.uri.sections', true))

  const elementNode = (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex align-items-center gap-2">
        <strong>{gettext('Section')}{':'}</strong>
        <div className="flex-grow-1">
          <Html html={section.title} />
        </div>

        <div className="d-flex align-items-center gap-1">
          <ReadOnlyIcon title={gettext('This section is read only')} show={section.read_only} />
          <NestedLink title={gettext('View section nested')} href={nestedUrl} onClick={fetchNested} show={display != 'nested'} />
          <ShowElementsLink showElements={showElements} show={display == 'nested'} onClick={toggleShowElements} />
          <EditLink title={gettext('Edit section')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy section')} href={copyUrl} onClick={fetchCopy} />
          <AddLink title={gettext('Add page')} onClick={createPage} disabled={section.read_only} />
          <LockedLink title={
            section.locked ? gettext('Unlock section'): gettext('Lock section')
          }
          locked={section.locked} onClick={toggleLocked} disabled={section.read_only} />
          <ExportLink title={gettext('Export section')} exportUrl={exportUrl}
            exportFormats={config.settings.export_formats} full={true} />
          <Drag element={section} show={display == 'nested'} />
        </div>
      </div>
      {
        displayUriSections &&
        <CodeLink type="questions" uri={section.uri} href={editUrl} onClick={() => fetchEdit()} order={order} />
      }
      <ElementErrors element={section} />
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
        <div className="position-relative">
          {
            showElement && (
              <Drop element={section}>
                <div className="card mt-2" style={{ marginLeft: `calc(${indent} * var(--indent-factor))` }}>
                  <div className="card-body">
                    { elementNode }
                  </div>
                </div>
              </Drop>
            )
          }
          {
            !isEmpty(section.elements) &&
            <Drop element={section.elements[0]} indent={indent + 1} mode="before"
              dropElement={(...args) => dispatch(dropElement(...args))} />
          }
          {
            showElements && section.elements.map((page, index) => {
              const pageInfo = section.pages.find(info => info.page === page.id)
              const pageOrder = pageInfo ? pageInfo.order : undefined

              return (
                <Page
                  key={index}
                  config={config}
                  page={page}
                  display="nested"
                  filter={filter}
                  indent={indent + 1}
                  order={pageOrder}
                />
              )
            })
          }
          <Drop element={section} indent={indent} mode="after" />
        </div>
      )
    case 'plain':
      return elementNode
  }
}

Section.propTypes = {
  section: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default Section
