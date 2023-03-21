import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, CreateButton, DeleteButton } from '../common/ElementButtons'

import DeleteSectionModal from '../modals/DeleteSectionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditSection = ({ config, section, elements, elementActions}) => {

  const { pages, catalogs } = elements

  const updateSection = (key, value) => elementActions.updateElement(section, key, value)
  const storeSection = () => elementActions.storeElement('sections', section)
  const deleteSection = () => elementActions.deleteElement('sections', section)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          {
            section.id ? <SaveButton onClick={storeSection} />
                       : <CreateButton onClick={storeSection} />
          }
        </div>
        {
          section.id ? <div>
            <strong>{gettext('Section')}{': '}</strong>
            <code className="code-questions">{section.uri}</code>
          </div> : <strong>{gettext('Create section')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={section} field="uri_prefix"
                       onChange={updateSection} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={section} field="uri_path"
                  onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={section} field="comment"
                      rows={4} onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={section} field="locked"
                      onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={section} field="pages"
                                options={pages} verboseName="page"
                                onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#section-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={section} field={`title_${lang_code }`}
                            onChange={updateSection} />
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
          {
            section.id ? <SaveButton onClick={storeSection} />
                       : <CreateButton onClick={storeSection} />
          }
        </div>
        {section.id && <DeleteButton onClick={openDeleteModal} />}
      </div>

      <DeleteSectionModal section={section} catalogs={catalogs.filter(e => section.catalogs.includes(e.id))}
                          show={showDeleteModal} onClose={closeDeleteModal} onDelete={deleteSection} />
    </div>
  )
}

EditSection.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditSection
