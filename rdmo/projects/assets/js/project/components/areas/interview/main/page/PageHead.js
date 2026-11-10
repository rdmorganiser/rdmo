import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import { isEmpty, isNil, upperFirst } from 'lodash'

import useModal from 'rdmo/core/assets/js/hooks/useModal'
import { selectReadOnly } from 'rdmo/projects/assets/js/common/selectors/permissions'

import LinkButton from 'rdmo/core/assets/js/components/LinkButton'

import { copySet, createSet, deleteSet, updateSet } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'
import { generateSetIndex } from '../../../../../utils/set'

import PageHeadDeleteModal from './PageHeadDeleteModal'
import PageHeadFormModal from './PageHeadFormModal'
import PageHeadReuseModal from './PageHeadReuseModal'
import PageHeadTabs from './PageHeadTabs'
import PageTabsHelp from './PageTabsHelp'

const PageHead = ({ sets, values, currentSet }) => {
  const dispatch = useDispatch()
  const page = useSelector((state) => state.interview.page)
  const readOnly = useSelector(selectReadOnly)

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
    dispatch(copySet(currentSet, copySetValue, currentSetValue))
    importModal.close()
  }

  return page.is_collection && (
    <>
      <PageTabsHelp />
      {
        currentSet ? (
          <div className="sticky-top bg-body d-flex align-items-center border-bottom border-2 mt-2 mb-4">
            <PageHeadTabs sets={sets} values={values} currentSet={currentSet} />
            {
              !readOnly && (
                <div>
                  <div className="d-flex gap-2 ms-3 pe-3">
                    <LinkButton className="bi bi-plus-lg" title={labels.add} onClick={createModal.open} />
                    {
                      page.attribute && (
                        <LinkButton className="bi bi-pencil" title={labels.edit} onClick={updateModal.open} />
                      )
                    }
                    <LinkButton className="bi bi-copy" title={labels.copy} onClick={copyModal.open} />
                    <LinkButton className="bi bi-arrow-down-circle" title={labels.reuse} onClick={importModal.open} />
                    <LinkButton className="bi bi-trash" title={labels.remove} onClick={deleteModal.open} />
                  </div>
                </div>
              )
            }
          </div>
        ) : (
          !readOnly && (
            <div className="d-flex justify-content-center border-bottom border-2 px-3 py-2 mt-2 mb-4">
              <LinkButton title={labels.add} onClick={createModal.open}>
                <i className="bi bi-plus" aria-hidden="true"></i> {upperFirst(page.verbose_name)}
              </LinkButton>
            </div>
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
    </>
  )
}

PageHead.propTypes = {
  sets: PropTypes.array,
  values: PropTypes.array,
  currentSet: PropTypes.object,
}

export default PageHead
