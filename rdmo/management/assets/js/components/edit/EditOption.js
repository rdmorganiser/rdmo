import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'

import { storeElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
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
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This option is read only')} show={option.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} back={true}/>
        </div>
        {
          option.id ? <>
            <strong>{gettext('Option')}{': '}</strong>
            <code className="code-options">{option.uri}</code>
          </> : <strong>{gettext('Create option')}</strong>
        }
      </div>

      {
        parent && parent.optionset && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This option will be added to the option set <code class="code-options">%s</code>.'), [parent.optionset.uri])
          }} />
        </div>
      }

      {
        option.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
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

        <Tabs id="#option-tabs" defaultActiveKey={0} animation={false}>
          {
            settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <div className="row">
                  <div className="col-sm-12">
                    <Text element={option} field={`text_${lang_code }`} onChange={updateOption} />
                    <Textarea element={option} field={`help_${lang_code }`} onChange={updateOption} />
                    <Textarea element={option} field={`view_text_${lang_code }`} onChange={updateOption} />
                  </div>
                </div>
              </Tab>
            ))
          }
        </Tabs>

        <Radio element={option} field="additional_input" options={additionalInputs} onChange={updateOption} />
        {
          (option.additional_input === 'text' || option.additional_input === 'textarea') &&
          settings && (
            <Tabs id="#option-tabs2" defaultActiveKey={0} animation={false}>
              {settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Textarea key={index} element={option} field={`default_text_${lang_code}`}
                          rows={1} onChange={updateOption} />
              </Tab>

            ))}
            </Tabs>
          )
        }

        {
          settings.multisite && (
            <Select element={option} field="editors" options={sites} onChange={updateOption} isMulti />
          )
        }

      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeOption} disabled={option.read_only} back={true}/>
        </div>
        {option.id && <DeleteButton onClick={openDeleteModal} disabled={option.read_only} />}
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
