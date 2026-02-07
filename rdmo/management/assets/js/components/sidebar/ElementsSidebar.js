import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isNil, isEmpty, invert } from 'lodash'

import Link from 'rdmo/core/assets/js/components/Link'
import Select from 'rdmo/core/assets/js/components/Select'

import { fetchElements } from '../../actions/elementActions'
import { uploadFile } from '../../actions/importActions'

import { elementTypes, elementModules } from '../../constants/elements'

import { buildApiPath, buildPath } from '../../utils/location'
import { getExportParams } from '../../utils/filter'


const ElementsSidebar = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const { elementType, elementId } = useSelector((state) => state.elements)

  const model = invert(elementTypes)[elementType]
  const exportUrl = isNil(elementId) ? buildApiPath(elementModules[model], elementType, 'export')
                                     : buildApiPath(elementModules[model], elementType, elementId, 'export')
  const exportParams = isNil(config.filter) ? '' : getExportParams(config.filter[elementType])

  const handleExport = (key) => {

    const getUrl = () => {
      let url = exportUrl

      if (key == 'xml') {
        url += '?'
      } else if (key == 'xml_full') {
        url += '?full=true'
      } else {
        url += `${key}?`
      }

      url += `&${exportParams}`

      return url
    }

    const a = document.createElement('a')
    a.href = getUrl()
    a.target = ['pdf', 'html'].includes(key) ? '_blank' : '_self'
    a.click()
  }

  const handleFileUpload = (event) => {
    if (!isEmpty(event.target.files)) {
      dispatch(uploadFile(event.target.files[0]))
    }
  }

  const navigation = {
    catalogs: gettext('Catalogs'),
    sections: gettext('Sections'),
    pages: gettext('Pages'),
    questionsets: gettext('Question sets'),
    questions: gettext('Questions'),
    attributes: gettext('Attributes'),
    optionsets: gettext('Option sets'),
    options: gettext('Options'),
    conditions: gettext('Conditions'),
    tasks: gettext('Tasks'),
    views: gettext('Views'),
  }

  const icons = {
    catalogs: 'book',
    sections: 'files',
    pages: 'file',
    questionsets: 'question-square',
    questions: 'question-circle',
    attributes: 'code-slash',
    optionsets: 'card-checklist',
    options: 'list-check',
    conditions: 'check-circle',
    tasks: 'exclamation-circle',
    views: 'file-earmark-text',
  }

  const exportOptions = [
    { value: 'xml', label: gettext('XML') }
  ]

  if ([
    'catalogs', 'sections', 'pages', 'questionsets', 'questions', 'optionsets', 'conditions', 'tasks'
  ].includes(elementType)) {
    exportOptions.push(
      { value: 'xml_full', label: gettext('XML (full)') }
    )
  }

  if (elementType == 'attributes') {
    exportOptions.push(
      { value: 'csvcomma', label: gettext('CSV comma separated') },
      { value: 'csvsemicolon', label: gettext('CSV semicolon separated') }
    )
  }

  if (config.settings.export_formats) {
    exportOptions.push(...config.settings.export_formats.map(([key, label]) => (
      { value: key, label }
    )))
  }

  return (
    <div className="d-flex flex-column h-100 p-4">
      <h2 className="px-3 mb-4">
        {gettext('Management')}
      </h2>

      <h3 className="px-3 mb-2">
        {gettext('Navigation')}
      </h3>

      <nav className="nav nav-pills nav-fill flex-column mb-4">
        {
          Object.entries(navigation).map(([et, label]) => (
            <Link key={et}
                  href={buildPath(et)}
                  className={classNames('nav-link text-start', { active: elementType === et })}
                  onClick={() => dispatch(fetchElements(et))}>
              <div className="d-flex align-items-center gap-2">
                <i className={`bi bi-${icons[et]}`} />
                {label}
              </div>
            </Link>
          ))
        }
      </nav>

      <h3 className="px-3 my-2">
        {gettext('Export')}
      </h3>

      <p className="text-muted px-3 my-2">
        {gettext('Export all visible elements.')}
      </p>

      <div className="text-muted px-3 mb-4">
        <Select options={exportOptions} onChange={handleExport} placeholder={gettext('Select format ...')}/>
      </div>

      <h3 className="px-3 mb-2">
        {gettext('Import')}
      </h3>

      <p className="text-muted px-3 mb-2">
        {gettext('Import an RDMO XML file.')}
      </p>

      <div className="text-muted px-3 mb-4">
        <input className="form-control" type="file" id="fileUpload" name="uploaded_file"
               onChange={handleFileUpload} />
      </div>
    </div>
  )
}

export default ElementsSidebar
