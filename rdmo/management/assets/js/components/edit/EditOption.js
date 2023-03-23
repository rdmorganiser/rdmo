import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, CreateButton, DeleteButton } from '../common/ElementButtons'

import OptionInfo from '../info/OptionInfo'
import DeleteOptionModal from '../modals/DeleteOptionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditOption = ({ config, option, elements, elementActions }) => {

  const { optionsets, conditions } = elements

  const optionConditions = conditions.filter(e => option.conditions.includes(e.id))

  const updateOption = (key, value) => elementActions.updateElement(option, key, value)
  const storeOption = () => elementActions.storeElement('options', option)
  const deleteOption = () => elementActions.deleteElement('options', option)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <OptionInfo option={option} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          {option.id ? <SaveButton onClick={storeOption} /> : <CreateButton onClick={storeOption} />}
        </div>
        {
          option.id ? <div>
            <strong>{gettext('Option')}{': '}</strong>
            <code className="code-options">{option.uri}</code>
          </div> : <strong>{gettext('Create option')}</strong>
        }
      </div>

      <div className="panel-body panel-border">
        { info }
      </div>

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
          <div className="col-sm-12">
            <Textarea config={config} element={option} field="comment"
                      rows={4} onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="locked"
                      onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="additional_input"
                      onChange={updateOption} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#option-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={option} field={`text_${lang_code }`}
                                onChange={updateOption} />
                        </div>
                      </div>
                    </Tab>
                  )
                })
              }
            </Tabs>
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          {option.id ? <SaveButton onClick={storeOption} /> : <CreateButton onClick={storeOption} />}
        </div>
        {option.id && <DeleteButton onClick={openDeleteModal} />}
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
