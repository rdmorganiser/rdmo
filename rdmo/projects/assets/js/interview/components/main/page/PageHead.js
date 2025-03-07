import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { capitalize, isEmpty, isNil, last } from 'lodash'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import PageHeadDeleteModal from './PageHeadDeleteModal'
import PageHeadFormModal from './PageHeadFormModal'
import PageHeadReuseModal from './PageHeadReuseModal'

import PageTabsHelp from './PageTabsHelp'

const PageHead = ({ templates, page, sets, values, disabled, currentSet,
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
      <PageTabsHelp templates={templates} page={page} disabled={disabled} />
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
              {
                !disabled && (
                  <li>
                    <a href="" title={gettext('Add tab')} className="add-set" onClick={handleOpenCreateModal}>
                      <i className="fa fa-plus fa-btn" aria-hidden="true"></i> {capitalize(page.verbose_name)}
                    </a>
                  </li>
                )
              }
            </ul>
            {
              !disabled && (
                <div className="interview-page-tabs-buttons">
                  {
                    page.attribute && (
                      <button type="button" className="btn-link fa fa-pencil"
                              title={gettext('Edit tab')} aria-label={gettext('Edit tab')}
                              onClick={updateModal.open} />
                    )
                  }
                  <button type="button" className="btn-link fa fa-copy"
                          title={gettext('Copy tab')} aria-label={gettext('Copy tab')}
                          onClick={copyModal.open} />
                  <button type="button" className="btn-link fa fa-arrow-circle-down"
                          title={gettext('Reuse answers')} aria-label={gettext('Reuse answers')}
                          onClick={importModal.open} />
                  <button type="button" className="btn-link fa fa-trash"
                          title={gettext('Remove tab')} aria-label={gettext('Remove tab')}
                          onClick={deleteModal.open} />
                </div>
              )
            }
          </>
        ) : (
          <button type="button" className="btn btn-success"
                  title={gettext('Add tab')} aria-label={gettext('Add tab')}
                  onClick={createModal.open}>
            <i className="fa fa-plus fa-btn" aria-hidden="true"></i> {capitalize(page.verbose_name)}
          </button>
        )
      }

      {
        !disabled && <>
        <PageHeadFormModal
          title={gettext('Create tab')}
          submitLabel={gettext('Create')}
          submitColor="success"
          show={createModal.show}
          attribute={page.attribute}
          reuse={true}
          onClose={createModal.close}
          onSubmit={handleCreate}
        />
        <PageHeadFormModal
          title={gettext('Copy tab')}
          submitLabel={gettext('Copy')}
          submitColor="info"
          show={copyModal.show}
          attribute={page.attribute}
          onClose={copyModal.close}
          onSubmit={handleCopy}
        />
        {
          currentSetValue && (
            <PageHeadFormModal
              title={gettext('Update tab')}
              submitLabel={gettext('Update')}
              submitColor="primary"
              show={updateModal.show}
              attribute={page.attribute}
              initial={currentSetValue.text}
              onClose={updateModal.close}
              onSubmit={handleUpdate}
            />
          )
        }
        {
          currentSetValue && (
            <PageHeadReuseModal
              show={importModal.show}
              attribute={page.attribute}
              onClose={importModal.close}
              onSubmit={handleImport}
            />
          )
        }
        <PageHeadDeleteModal
          name={currentSetValue ? currentSetValue.text : null}
          show={deleteModal.show}
          onClose={deleteModal.close}
          onSubmit={handleDelete}
        />
      </>
    }
    </div>
  )
}

PageHead.propTypes = {
  templates: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool.isRequired,
  currentSet: PropTypes.object,
  activateSet: PropTypes.func.isRequired,
  createSet: PropTypes.func.isRequired,
  updateSet: PropTypes.func.isRequired,
  deleteSet: PropTypes.func.isRequired,
  copySet: PropTypes.func.isRequired
}

export default PageHead
