import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

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

const EditOptionSet = ({ config, optionset, elements, elementActions }) => {

  const { sites, providers } = config
  const { elementAction, parent, conditions, options } = elements

  const updateOptionSet = (key, value) => elementActions.updateElement(optionset, {[key]: value})
  const storeOptionSet = (back) => elementActions.storeElement('optionsets', optionset, elementAction, back)
  const deleteOptionSet = () => elementActions.deleteElement('optionsets', optionset)

  const editOption = (value) => elementActions.fetchElement('options', value.option)
  const createOption = () => elementActions.createElement('options', { optionset })

  const editCondition = (condition) => elementActions.fetchElement('conditions', condition)
  const createCondition = () => elementActions.createElement('conditions', { optionset })

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <OptionSetInfo optionset={optionset} elements={elements} elementActions={elementActions} />

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
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This option set will be added to the question <code class="code-questions">%s</code>.'), [parent.question.uri])
          }} />
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
            <UriPrefix config={config} element={optionset} field="uri_prefix"
                       onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={optionset} field="uri_path"
                  onChange={updateOptionSet} />
          </div>
        </div>

        <Textarea config={config} element={optionset} field="comment"
                  rows={4} onChange={updateOptionSet} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox config={config} element={optionset} field="locked"
                      onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Number config={config} element={optionset} field="order"
                    onChange={updateOptionSet} />
          </div>
        </div>

        <OrderedMultiSelect config={config} element={optionset} field="options" options={options}
                            addText={gettext('Add existing option')} createText={gettext('Create new option')}
                            onChange={updateOptionSet} onCreate={createOption} onEdit={editOption} />

        <MultiSelect config={config} element={optionset} field="conditions" options={conditions}
                     addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                     onChange={updateOptionSet} onCreate={createCondition} onEdit={editCondition} />

        <Select config={config} element={optionset} field="provider_key"
                options={providers} onChange={updateOptionSet} />

        {get(config, 'settings.multisite') && <Select config={config} element={optionset} field="editors"
                                                      options={sites} onChange={updateOptionSet} isMulti />}
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
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditOptionSet
