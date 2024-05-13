import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { capitalize, isNil, last } from 'lodash'

import Template from 'rdmo/core/assets/js/components/Template'
import useModal from 'rdmo/core/assets/js/hooks/useModal'

import PageHeadDeleteModal from './PageHeadDeleteModal'
import PageHeadFormModal from './PageHeadFormModal'

const PageHead = ({ page, help, sets, values, currentSet, activateSet, createSet, updateSet, deleteSet }) => {

  const currentSetValue = isNil(currentSet) ? null : (
    values.find((value) => (
      value.set_prefix == currentSet.set_prefix && value.set_index == currentSet.set_index
    ))
  )

  const [showCreateModal, openCreateModal, closeCreateModal] = useModal()
  const [showUpdateModal, openUpdateModal, closeUpdateModal] = useModal()
  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useModal()

  const handleActivateSet = (event, set) => {
    event.preventDefault()
    if (set.set_index != currentSet.set_index) {
      activateSet(set)
    }
  }

  const handleCreateSet = (text) => {
    createSet({
      attribute: page.attribute,
      set_index: last(sets) ? last(sets).set_index + 1 : 0,
      set_collection: page.is_collection,
      text
    })
    closeCreateModal()
  }

  const handleUpdateSet = (text) => {
    updateSet(currentSetValue, { text })
    closeUpdateModal()
  }

  const handleDeleteSet = () => {
    deleteSet(currentSet, currentSetValue)
    closeDeleteModal()
  }

  return page.is_collection && (
    <div className="interview-page-tabs">
      <Template template={help} />
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
                      <a href="#" onClick={(event) => handleActivateSet(event, set)}>
                        {isNil(setValue) ? `#${set.set_index + 1}` : setValue.text}
                      </a>
                    </li>
                  )
                })
              }
              <li>
                <a href="#" title={gettext('Add tab')} className="add-set" onClick={openCreateModal}>
                  <i className="fa fa-plus fa-btn"></i> {capitalize(page.verbose_name)}
                </a>
              </li>
            </ul>
            <div className="interview-page-tabs-buttons">
                {
                  page.attribute && (
                    <button className="btn-link fa fa-pencil" title={gettext('Edit tab')} onClick={openUpdateModal} />
                  )
                }
                <button className="btn-link fa fa-trash" title={gettext('Remove tab')} onClick={openDeleteModal} />
            </div>
          </>
        ) : (
          <button className="btn btn-success" title={gettext('Add tab')} onClick={openCreateModal}>
            <i className="fa fa-plus fa-btn"></i> {capitalize(page.verbose_name)}
          </button>
        )
      }

      <PageHeadFormModal
        title={capitalize(page.verbose_name)}
        show={showCreateModal}
        initial={isNil(page.attribute) ? null : ''}
        onClose={closeCreateModal}
        onSubmit={handleCreateSet}
      />
      {
        currentSetValue && (
          <PageHeadFormModal
            title={capitalize(page.verbose_name)}
            show={showUpdateModal}
            initial={currentSetValue.text}
            onClose={closeUpdateModal}
            onSubmit={handleUpdateSet}
          />
        )
      }
      <PageHeadDeleteModal
        title={capitalize(page.verbose_name)}
        show={showDeleteModal}
        onClose={closeDeleteModal}
        onSubmit={handleDeleteSet}
      />
    </div>
  )
}

PageHead.propTypes = {
  page: PropTypes.object.isRequired,
  help: PropTypes.string.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  currentSet: PropTypes.object,
  activateSet: PropTypes.func.isRequired,
  createSet: PropTypes.func.isRequired,
  updateSet: PropTypes.func.isRequired,
  deleteSet: PropTypes.func.isRequired
}

export default PageHead