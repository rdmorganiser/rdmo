import React from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'
import get from 'lodash/get'

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

const EditOption = ({ config, option, elements, elementActions }) => {

  const { additionalInputs, sites } = config
  const { elementAction, parent } = elements

  const updateOption = (key, value) => elementActions.updateElement(option, {[key]: value})
  const storeOption = (back) => elementActions.storeElement('options', option, back)
  const deleteOption = () => elementActions.deleteElement('options', option)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <OptionInfo option={option} elements={elements} elementActions={elementActions} />

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
            <UriPrefix config={config} element={option} field="uri_prefix"
                       onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={option} field="uri_path"
                  onChange={updateOption} />
          </div>
        </div>

        <Textarea config={config} element={option} field="comment"
                  rows={4} onChange={updateOption} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="locked"
                      onChange={updateOption} />
          </div>
        </div>

        <Tabs id="#option-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <div className="row">
                  <div className="col-sm-12">
                    <Text config={config} element={option} field={`text_${lang_code }`}
                          onChange={updateOption} />
                  </div>
                </div>
              </Tab>
            ))
          }
        </Tabs>

        <Radio config={config} element={option} field="additional_input"
               options={additionalInputs} onChange={updateOption} />

        {get(config, 'settings.multisite') && <Select config={config} element={option} field="editors"
                                                      options={sites} onChange={updateOption} isMulti />}
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
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditOption
