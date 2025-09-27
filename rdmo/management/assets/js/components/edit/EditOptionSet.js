import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement, storeElement, createElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import Number from './common/Number'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import MultiSelect from './common/MultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import OptionSetInfo from '../info/OptionSetInfo'
import DeleteOptionSetModal from '../modals/DeleteOptionSetModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditOptionSet = ({ optionset }) => {
  const dispatch = useDispatch()

  const { sites, providers, settings } = useSelector((state) => state.config)
  const { elementAction, parent, conditions, options } = useSelector((state) => state.elements)

  const updateOptionSet = (key, value) => dispatch(updateElement(optionset, {[key]: value}))
  const storeOptionSet = (back) => dispatch(storeElement('optionsets', optionset, elementAction, back))
  const deleteOptionSet = () => dispatch(deleteElement('optionsets', optionset))

  const editOption = (value) => dispatch(fetchElement('options', value.option))
  const createOption = () => dispatch(createElement('options', { optionset }))

  const editCondition = (condition) => dispatch(fetchElement('conditions', condition))
  const createCondition = () => dispatch(createElement('conditions', { optionset }))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <OptionSetInfo optionset={optionset} />

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This option set is read only')} show={optionset.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeOptionSet} disabled={optionset.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeOptionSet} disabled={optionset.read_only} back={true}/>
        </div>
        {
          optionset.id ? <>
            <strong>{gettext('Option set')}{': '}</strong>
            <code className="code-options">{optionset.uri}</code>
          </> : <strong>{gettext('Create option set')}</strong>
        }
      </div>

      {
        parent && parent.question && <div className="panel-body panel-border">
        <Html html={interpolate(gettext(
          'This option set will be added to the question <code class="code-questions">%s</code>.'),
          [parent.question.uri])} />
        </div>
      }

      {
        optionset.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={optionset} field="uri_prefix" onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Text element={optionset} field="uri_path" onChange={updateOptionSet} />
          </div>
        </div>

        <Textarea element={optionset} field="comment" rows={4} onChange={updateOptionSet} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox element={optionset} field="locked" onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Number element={optionset} field="order" onChange={updateOptionSet} />
          </div>
        </div>

        <OrderedMultiSelect element={optionset} field="options" options={options}
                            addText={gettext('Add existing option')} createText={gettext('Create new option')}
                            onChange={updateOptionSet} onCreate={createOption} onEdit={editOption} />

        <MultiSelect element={optionset} field="conditions" options={conditions}
                     addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                     onChange={updateOptionSet} onCreate={createCondition} onEdit={editCondition} />

        <Select element={optionset} field="provider_key" options={providers} onChange={updateOptionSet} />

        {
          settings.multisite && (
            <Select element={optionset} field="editors"
                    options={sites} onChange={updateOptionSet} isMulti />
          )
        }
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeOptionSet} disabled={optionset.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeOptionSet} disabled={optionset.read_only} back={true}/>
        </div>
        {optionset.id && <DeleteButton onClick={openDeleteModal} disabled={optionset.read_only} />}
      </div>

      <DeleteOptionSetModal optionset={optionset} info={info} show={showDeleteModal}
                            onClose={closeDeleteModal} onDelete={deleteOptionSet} />
    </div>
  )
}

EditOptionSet.propTypes = {
  optionset: PropTypes.object.isRequired
}

export default EditOptionSet
