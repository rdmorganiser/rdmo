import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import MultiSelect from '../forms/MultiSelect'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, CreateButton, DeleteButton } from '../common/ElementButtons'

import PageInfo from '../info/PageInfo'
import DeletePageModal from '../modals/DeletePageModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditPage = ({ config, page, elements, elementActions }) => {

  const { attributes, conditions, sections, questionsets, questions } = elements

  const pageSections = sections.filter(e => page.sections.includes(e.id))

  const updatePage = (key, value) => elementActions.updateElement(page, key, value)
  const storePage = () => elementActions.storeElement('pages', page)
  const deletePage = () => elementActions.deleteElement('pages', page)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <PageInfo page={page} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          {
            page.id ? <SaveButton onClick={storePage} />
                    : <CreateButton onClick={storePage} />
          }
        </div>
        {
          page.id ? <div>
            <strong>{gettext('Page')}{': '}</strong>
            <code className="code-questions">{page.uri}</code>
          </div> : <strong>{gettext('Create page')}</strong>
        }
      </div>

      <div className="panel-body panel-border">
        { info }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={page} field="uri_prefix"
                  onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={page} field="uri_path"
                  onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={page} field="comment"
                      rows={4} onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={page} field="locked"
                      onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={page} field="is_collection"
                      onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={page} field="attribute"
                    options={attributes} onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={page} field="questionsets"
                                options={questionsets} verboseName="questionset"
                                onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={page} field="questions"
                                options={questions} verboseName="question"
                                onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <MultiSelect config={config} element={page} field="conditions"
                         options={conditions} verboseName="condition"
                         onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={page} field={`title_${lang_code }`}
                                onChange={updatePage} />
                        </div>
                        <div className="col-sm-12">
                          <Textarea config={config} element={page} field={`help_${lang_code }`}
                                    rows={4} onChange={updatePage} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={page} field={`verbose_name_${lang_code }`}
                                onChange={updatePage} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={page} field={`verbose_name_plural_${lang_code }`}
                                onChange={updatePage} />
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
          {
            page.id ? <SaveButton onClick={storePage} />
                    : <CreateButton onClick={storePage} />
          }
        </div>
        {page.id && <DeleteButton onClick={openDeleteModal} />}
      </div>

      <DeletePageModal page={page} info={info} show={showDeleteModal}
                       onClose={closeDeleteModal} onDelete={deletePage} />
    </div>
  )
}

EditPage.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditPage
