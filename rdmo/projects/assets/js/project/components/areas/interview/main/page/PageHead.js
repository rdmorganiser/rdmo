import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty, isNil, upperFirst } from 'lodash'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import LinkButton from 'rdmo/core/assets/js/components/LinkButton'

import { activateSet, copySet, createSet, deleteSet, updateSet } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'
import { generateSetIndex } from '../../../../../utils/set'

import PageHeadDeleteModal from './PageHeadDeleteModal'
import PageHeadFormModal from './PageHeadFormModal'
import PageHeadReuseModal from './PageHeadReuseModal'
import PageTabsHelp from './PageTabsHelp'

const PageHead = ({ sets, values, currentSet }) => {
  const dispatch = useDispatch()
  const page = useSelector((state) => state.interview.page)
  const readOnly = useReadOnly()

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

  // inlining the title attributes caused problems with django's translation system
  const labels = {
    copy: gettext('Copy tab'),
    add: gettext('Add tab'),
    edit: gettext('Edit tab'),
    reuse: gettext('Reuse answers'),
    remove: gettext('Remove tab')
  }

  const handleActivate = (event, set) => {
    event.preventDefault()
    if (set.set_index != currentSet.set_index) {
      dispatch(activateSet(set))
    }
  }

  const handleOpenCreateModal = (event) => {
    event.preventDefault()
    createModal.open()
  }

  const handleCreate = (text, copySetValue) => {
    if (isEmpty(copySetValue)) {
      dispatch(createSet({
        attribute: page.attribute,
        set_index: generateSetIndex(sets, currentSet),
        set_collection: page.is_collection,
        element: page,
        text
      }))
    } else {
      // TODO: check if this code is ever executed
      dispatch(copySet(currentSet, copySetValue, {
        attribute: page.attribute,
        set_index: generateSetIndex(sets, currentSet),
        set_collection: page.is_collection,
        element: page,
        text
      }))
    }
    createModal.close()
  }

  const handleUpdate = (text) => {
    dispatch(updateSet(currentSetValue, { text }))
    updateModal.close()
  }

  const handleDelete = () => {
    dispatch(deleteSet(currentSet, currentSetValue))
    deleteModal.close()
  }

  const handleCopy = (text) => {
    dispatch(copySet(currentSet, currentSetValue, {
      attribute: page.attribute,
      set_index: generateSetIndex(sets, currentSet),
      set_collection: page.is_collection,
      element: page,
      text
    }))
    copyModal.close()
  }

  const handleImport = (copySetValue) => {
    copySet(currentSet, copySetValue, currentSetValue)
    importModal.close()
  }

  return page.is_collection && (
    <div className="project-interview-page-head">
      <div className="d-flex flex-column justify-content-between gap-2">
        <PageTabsHelp />
        {
          currentSet ? (
            <>
              <ul className="nav nav-tabs">
                {
                  sets.map((set, setIndex) => {
                    const setValue = values.find((value) => (
                      value.set_prefix == set.set_prefix && value.set_index == set.set_index
                    ))
                    const setLabel = isNil(setValue) ? `#${set.set_index + 1}` : setValue.text
                    return (
                      <li key={setIndex} className="nav-item">
                        <a
                          href=""
                          title={setLabel}
                          className={classNames('nav-link', {active: set.set_index == currentSet.set_index})}
                          onClick={(event) => handleActivate(event, set)}
                        >
                          {setLabel}
                        </a>
                      </li>
                    )
                  })
                }
                {
                  !readOnly && (
                    <li>
                      <a
                        href=""
                        title={labels.add}
                        className="nav-link add-set"
                        onClick={handleOpenCreateModal}
                      >
                        <i className="bi bi-plus" aria-hidden="true"></i> {upperFirst(page.verbose_name)}
                      </a>
                    </li>
                  )
                }
              </ul>
              {
                !readOnly && (
                  <div className="d-flex justify-content-end gap-1">
                    {
                      page.attribute && (
                        <LinkButton
                          className="bi bi-pencil"
                          title={labels.edit}
                          aria-label={labels.copy}
                          onClick={updateModal.open}
                        />
                      )
                    }
                    <LinkButton
                      className="bi bi-copy"
                      title={labels.copy}
                      aria-label={labels.copy}
                      onClick={copyModal.open}
                    />
                    <LinkButton
                      className="bi bi-arrow-down-circle"
                      title={labels.reuse}
                      aria-label={labels.reuse}
                      onClick={importModal.open}
                    />
                    <LinkButton
                      className="bi bi-trash"
                      title={labels.remove}
                      aria-label={labels.remove}
                      onClick={deleteModal.open}
                    />
                  </div>
                )
              }
            </>
          ) : (
            !readOnly && (
              <button role="button" className="btn btn-success" title={labels.add} onClick={createModal.open}>
                <i className="bi bi-plus" aria-hidden="true"></i> {upperFirst(page.verbose_name)}
              </button>
            )
          )
        }

        {
          !readOnly && (
            <>
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
          )
        }
      </div>
    </div>
  )
}

PageHead.propTypes = {
  sets: PropTypes.array,
  values: PropTypes.array,
  currentSet: PropTypes.object,
}

export default PageHead
