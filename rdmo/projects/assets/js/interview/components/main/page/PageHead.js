import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { capitalize, isEmpty, isNil, last } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'
import useModal from 'rdmo/core/assets/js/hooks/useModal'

import PageHeadDeleteModal from './PageHeadDeleteModal'
import PageHeadFormModal from './PageHeadFormModal'
import PageHeadImportModal from './PageHeadImportModal'

const PageHead = ({ templates, page, sets, values, currentSet,
                    activateSet, createSet, updateSet, deleteSet, copySet }) => {

  const currentSetValue = isNil(currentSet) ? null : (
    values.find((value) => (
      value.set_prefix == currentSet.set_prefix && value.set_index == currentSet.set_index
    ))
  )

  const createModal = useModal()
  const updateModal = useModal()
  const copyModal = useModal()
  const importModal = useModal()
  const deleteModal = useModal()

  const handleActivate = (event, set) => {
    event.preventDefault()
    if (set.set_index != currentSet.set_index) {
      activateSet(set)
    }
  }

  const handleOpenCreateModal = (event) => {
    event.preventDefault()
    createModal.open()
  }

  const handleCreate = (text, copySetValue) => {
    if (isEmpty(copySetValue)) {
      createSet({
        attribute: page.attribute,
        set_index: last(sets) ? last(sets).set_index + 1 : 0,
        set_collection: page.is_collection,
        text
      })
    } else {
      copySet(currentSet, copySetValue, {
        attribute: page.attribute,
        set_index: last(sets) ? last(sets).set_index + 1 : 0,
        set_collection: page.is_collection,
        text
      })
    }
    createModal.close()
  }

  const handleUpdate = (text) => {
    updateSet(currentSetValue, { text })
    updateModal.close()
  }

  const handleDelete = () => {
    deleteSet(currentSet, currentSetValue)
    deleteModal.close()
  }

  const handleCopy = (text) => {
    copySet(currentSet, currentSetValue, {
      attribute: page.attribute,
      set_index: last(sets) ? last(sets).set_index + 1 : 0,
      set_collection: page.is_collection,
      text
    })
    copyModal.close()
  }

  const handleImport = (copySetValue) => {
    copySet(currentSet, copySetValue, currentSetValue)
    importModal.close()
  }

  return page.is_collection && (
    <div className="interview-page-tabs">
      <Html html={templates.project_interview_page_help} />
      <Html html={templates.project_interview_page_tabs_help} />
      {
        currentSet ? (
          <>
            <ul className="nav nav-tabs">
              {
                sets.map((set, setIndex) => {
                  const setValue = values.find((value) => (
                    value.set_prefix == set.set_prefix && value.set_index == set.set_index
                  ))
                  return (
                    <li key={setIndex} className={classNames({active: set.set_index == currentSet.set_index})}>
                      <a href="#" onClick={(event) => handleActivate(event, set)}>
                        {isNil(setValue) ? `#${set.set_index + 1}` : setValue.text}
                      </a>
                    </li>
                  )
                })
              }
              <li>
                <a href="" title={gettext('Add tab')} className="add-set" onClick={handleOpenCreateModal}>
                  <i className="fa fa-plus fa-btn"></i> {capitalize(page.verbose_name)}
                </a>
              </li>
            </ul>
            <div className="interview-page-tabs-buttons">
              {
                page.attribute && (
                  <button className="btn-link fa fa-pencil" title={gettext('Edit tab')} onClick={updateModal.open} />
                )
              }
              <button className="btn-link fa fa-copy" title={gettext('Copy tab')} onClick={copyModal.open} />
              <button className="btn-link fa fa-arrow-circle-down" title={gettext('Import from tab')} onClick={importModal.open} />
              <button className="btn-link fa fa-trash" title={gettext('Remove tab')} onClick={deleteModal.open} />
            </div>
          </>
        ) : (
          <button className="btn btn-success" title={gettext('Add tab')} onClick={createModal.open}>
            <i className="fa fa-plus fa-btn"></i> {capitalize(page.verbose_name)}
          </button>
        )
      }

      <PageHeadFormModal
        title={capitalize(page.verbose_name)}
        submitLabel={gettext('Create')}
        submitColor="success"
        show={createModal.show}
        attribute={page.attribute}
        initial={{ text: '', copySetValue: '', snapshot: false }}
        onClose={createModal.close}
        onSubmit={handleCreate}
      />
      <PageHeadFormModal
        title={capitalize(page.verbose_name)}
        submitLabel={gettext('Copy')}
        submitColor="info"
        show={copyModal.show}
        attribute={page.attribute}
        initial={{ text: '' }}
        onClose={copyModal.close}
        onSubmit={handleCopy}
      />
      {
        currentSetValue && (
          <PageHeadFormModal
            title={capitalize(page.verbose_name)}
            submitLabel={gettext('Update')}
            submitColor="primary"
            show={updateModal.show}
            attribute={page.attribute}
            initial={{ text: currentSetValue.text }}
            onClose={updateModal.close}
            onSubmit={handleUpdate}
          />
        )
      }
      {
        currentSetValue && (
          <PageHeadImportModal
            title={capitalize(page.verbose_name)}
            show={importModal.show}
            attribute={page.attribute}
            onClose={importModal.close}
            onSubmit={handleImport}
          />
        )
      }
      <PageHeadDeleteModal
        title={capitalize(page.verbose_name)}
        name={currentSetValue ? currentSetValue.text : null}
        show={deleteModal.show}
        onClose={deleteModal.close}
        onSubmit={handleDelete}
      />
    </div>
  )
}

PageHead.propTypes = {
  templates: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  currentSet: PropTypes.object,
  activateSet: PropTypes.func.isRequired,
  createSet: PropTypes.func.isRequired,
  updateSet: PropTypes.func.isRequired,
  deleteSet: PropTypes.func.isRequired,
  copySet: PropTypes.func.isRequired
}

export default PageHead
