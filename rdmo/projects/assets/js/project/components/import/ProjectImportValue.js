import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { ShowLink } from 'rdmo/management/assets/js/components/common/Links'
import Errors from 'rdmo/management/assets/js/components/import/common/Errors'
import FieldRowDiffs from 'rdmo/management/assets/js/components/import/common/FieldRowDiffs'
import Warnings from 'rdmo/management/assets/js/components/import/common/Warnings'

import { updateValue } from '../../actions/importActions'

const ProjectImportValue = ({ value }) => {
  const dispatch = useDispatch()
  const disabled = value.errors.length > 0
  const showDiff = value.updated && value.changed

  const update = (changes) => dispatch(updateValue(value, changes))

  return (
    <li className="list-group-item">
      <div className="d-flex align-items-center gap-2">
        <div className="form-check">
          <input
            type="checkbox"
            className="form-check-input"
            checked={value.import}
            disabled={disabled}
            aria-label={gettext('Import value')}
            onChange={() => update({ import: !value.import })}
          />
        </div>

        <button
          type="button"
          className="btn link text-start flex-grow-1 p-0"
          onClick={() => update({ show: !value.show })}
        >
          <span>{value.question_text || gettext('Question not available')}</span>
          <code className="d-block small mt-1">{value.attribute_uri}</code>
        </button>

        {
          showDiff && <span className="badge text-bg-info">{gettext('Changed')}</span>
        }
        {
          value.created && <span className="badge text-bg-success">{gettext('New')}</span>
        }

        <ShowLink show={value.show} onClick={() => update({ show: !value.show })} />
      </div>

      {
        value.show && (
          <div className="mt-3">
            <Errors elementErrors={value.errors} />
            <Warnings
              elementWarnings={value.warnings}
              elementModel={value.model}
              elementURI={value.uri}
              shouldShowURI={false}
            />
            {
              showDiff ? (
                <FieldRowDiffs element={value} field="value_and_unit" />
              ) : (
                <div className="import-card card mb-2">
                  <div className="card-body">
                    <code className="d-block mb-2">{gettext('Imported answer')}</code>
                    <span>{value.value_and_unit}</span>
                  </div>
                </div>
              )
            }
          </div>
        )
      }
    </li>
  )
}

ProjectImportValue.propTypes = {
  value: PropTypes.object.isRequired
}

export default ProjectImportValue
