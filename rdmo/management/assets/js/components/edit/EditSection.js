import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { createElement, deleteElement, fetchElement, storeElement, updateElement } from '../../actions/elementActions'
import useDeleteModal from '../../hooks/useDeleteModal'

import { BackButton, DeleteButton, SaveButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'
import SectionInfo from '../info/SectionInfo'
import DeleteSectionModal from '../modals/DeleteSectionModal'

import Checkbox from './common/Checkbox'
import LanguageTabs from './common/LanguageTabs'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

const EditSection = ({ section }) => {
  const dispatch = useDispatch()

  const { sites, settings } = useSelector((state) => state.config)
  const { elementAction, parent, pages } = useSelector((state) => state.elements)

  const updateSection = (key, value) => dispatch(updateElement(section, {[key]: value}))
  const storeSection = (back) => dispatch(storeElement('sections', section, elementAction, back))
  const deleteSection = () => dispatch(deleteElement('sections', section))

  const editPage = (value) => dispatch(fetchElement('pages', value.page))
  const createPage = () => dispatch(createElement('pages', { section }))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <SectionInfo section={section} />

  // for reasons unknown, the strings are not picked up by makemessages from the props
  const addPageText = gettext('Add existing page')
  const createPageText = gettext('Create new page')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-wrap align-items-center gap-2">
          <strong className="flex-grow-1">
            {section.id ? gettext('Edit section') : gettext('Create section')}
          </strong>
          <ReadOnlyIcon title={gettext('This section is read only')} show={section.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeSection} disabled={section.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeSection} disabled={section.read_only} back={true}/>
        </div>
      </div>

      {
        parent && parent.catalog && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This section will be added to the catalog <code class="code-questions">%s</code>.'),
              [parent.catalog.uri])
            } />
          </div>
        )
      }

      {
        section.id && (
          <div className="card-body border-bottom">
            {info}
          </div>
        )
      }

      <div className="card-body pb-0">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={section} field="uri_prefix" onChange={updateSection} />
          </div>
          <div className="col-sm-6">
            <Text element={section} field="uri_path" onChange={updateSection} />
          </div>
        </div>

        <Textarea element={section} field="comment" rows={4} onChange={updateSection} />

        <Checkbox element={section} field="locked" onChange={updateSection} />

        <LanguageTabs render={
          (langCode) => (
            <div>
              <Text element={section} field={`title_${langCode}`} onChange={updateSection} />
              <Text element={section} field={`short_title_${langCode}`} onChange={updateSection} />
            </div>
          )
        } />

        <OrderedMultiSelect
          element={section} field="pages" options={pages}
          addText={addPageText} createText={createPageText}
          onChange={updateSection} onCreate={createPage} onEdit={editPage} />

        {
          settings.multisite && (
            <Select element={section} field="editors" options={sites} onChange={updateSection} isMulti />
          )
        }
      </div>

      <div className="card-footer">
        <div className="d-flex align-items-center gap-2">
          {section.id && <DeleteButton onClick={openDeleteModal} disabled={section.read_only} />}
          <BackButton className="ms-auto" />
          <SaveButton elementAction={elementAction} onClick={storeSection} disabled={section.read_only}  />
          <SaveButton elementAction={elementAction} onClick={storeSection} disabled={section.read_only} back={true}/>
        </div>
      </div>

      <DeleteSectionModal
        section={section} info={info} show={showDeleteModal}
        onClose={closeDeleteModal} onDelete={deleteSection} />
    </div>
  )
}

EditSection.propTypes = {
  section: PropTypes.object.isRequired
}

export default EditSection
