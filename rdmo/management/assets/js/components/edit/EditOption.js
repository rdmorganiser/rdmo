import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import { storeElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import LanguageTabs from './common/LanguageTabs'
import Radio from './common/Radio'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import OptionInfo from '../info/OptionInfo'
import DeleteOptionModal from '../modals/DeleteOptionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditOption = ({ option }) => {
  const dispatch = useDispatch()

  const { additionalInputs, sites, settings } = useSelector((state) => state.config)
  const { elementAction, parent } = useSelector((state) => state.elements)

  const updateOption = (key, value) => dispatch(updateElement(option, {[key]: value}))
  const storeOption = (back) => dispatch(storeElement('options', option, elementAction, back))
  const deleteOption = () => dispatch(deleteElement('options', option))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <OptionInfo option={option} />

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-wrap align-items-center gap-2">
          <strong className="flex-grow-1">
            {option.id ? gettext('Edit option') : gettext('Create option')}
          </strong>
          <ReadOnlyIcon title={gettext('This option is read only')} show={option.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} back={true}/>
        </div>
      </div>

      {
        parent && parent.optionset && <div className="card-body border-bottom">
          <Html html={interpolate(gettext(
            'This option will be added to the option set <code class="code-options">%s</code>.'),
            [parent.optionset.uri])} />
        </div>
      }

      {
        option.id && <div className="card-body border-bottom">
          { info }
        </div>
      }

      <div className="card-body pb-0">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={option} field="uri_prefix" onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Text element={option} field="uri_path" onChange={updateOption} />
          </div>
        </div>

        <Textarea element={option} field="comment" rows={4} onChange={updateOption} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox element={option} field="locked" onChange={updateOption} />
          </div>
        </div>

        <LanguageTabs render={(langCode) => (
          <>
            <Text element={option} field={`text_${langCode}`} onChange={updateOption} />
            <Textarea element={option} field={`help_${langCode }`} onChange={updateOption} />
            <Textarea element={option} field={`view_text_${langCode}`} onChange={updateOption} />
          </>
        )} />

        <Radio element={option} field="additional_input" options={additionalInputs} onChange={updateOption} />
        {
          (option.additional_input === 'text' || option.additional_input === 'textarea') &&
          settings && (
            <LanguageTabs render={(langCode) => (
              <Textarea element={option} field={`default_text_${langCode}`} rows={1} onChange={updateOption} />
            )} />
          )
        }

        {
          settings.multisite && (
            <Select element={option} field="editors" options={sites} onChange={updateOption} isMulti />
          )
        }

      </div>

      <div className="card-footer">
        <div className="d-flex align-items-center gap-2">
          {option.id && <DeleteButton onClick={openDeleteModal} disabled={option.read_only} />}
          <BackButton className="ms-auto" />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} back={true}/>
        </div>
      </div>

      <DeleteOptionModal option={option} info={info} show={showDeleteModal}
                         onClose={closeDeleteModal} onDelete={deleteOption} />
    </div>
  )
}

EditOption.propTypes = {
  option: PropTypes.object.isRequired
}

export default EditOption
