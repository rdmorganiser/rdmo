import React from 'react'
import PropTypes from 'prop-types'

import { get } from 'lodash'
import DatePicker from 'react-datepicker'
import { formatISO } from 'date-fns'

import { Select } from 'rdmo/core/assets/js/components'
import useDatePicker from '../../hooks/useDatePicker'
import { language } from 'rdmo/core/assets/js/utils'

const ProjectFilters = ({ catalogs, config, configActions, isManager, projectsActions }) => {
  const {
    dateRange,
    dateFormat,
    getLocale,
    setStartDate,
    setEndDate
  } = useDatePicker()

  const catalogOptions = catalogs?.map(catalog => ({ value: catalog.id.toString(), label: catalog.title }))
  const selectedCatalog = get(config, 'params.catalog', '')
  const updateCatalogFilter = (value) => {
    value ? configActions.updateConfig('params.catalog', value) : configActions.deleteConfig('params.catalog')
    projectsActions.fetchAllProjects()
  }

  return (
    <div className="panel panel-default panel-filters mt-10 mb-0">
      <div className="panel-body">
        <div className="row">
          <div className={`col-md-${isManager ? 4 : 8}`}>
            <label className="control-label text-muted">{gettext('Filter by catalog')}</label>
            <div className="search-container">
              <Select
                className="select-custom"
                onChange={updateCatalogFilter}
                options={catalogOptions ?? []}
                placeholder={gettext('Select catalog')}
                value={selectedCatalog}
              />
            </div>
          </div>
          {isManager && (
            <div className="col-md-4">
              <label className="control-label text-muted">{gettext('Filter by created date')}</label>
              <div className="projects-datepicker">
                <div className="row">
                  <div className="col-md-6">
                    <DatePicker
                      autoComplete="off"
                      className="form-control"
                      dateFormat={dateFormat}
                      id="created-start-date-picker"
                      isClearable
                      locale={getLocale(language)}
                      onChange={date => {
                        setStartDate('created', date)
                        if (date) {
                          configActions.updateConfig('params.created_after', formatISO(date, { representation: 'date' }))
                        } else {
                          configActions.deleteConfig('params.created_after')
                        }
                        projectsActions.fetchAllProjects()
                      }}
                      placeholderText={gettext('Select start date')}
                      selected={dateRange.createdStart ?? get(config, 'params.created_after', '')}
                    />
                  </div>
                  <div className="col-md-6">
                    <DatePicker
                      autoComplete="off"
                      className="form-control"
                      dateFormat={dateFormat}
                      id="created-end-date-picker"
                      isClearable
                      locale={getLocale(language)}
                      onChange={date => {
                        setEndDate('created', date)
                        if (date) {
                          configActions.updateConfig('params.created_before', formatISO(date, { representation: 'date' }))
                        } else {
                          configActions.deleteConfig('params.created_before')
                        }
                        projectsActions.fetchAllProjects()
                      }}
                      placeholderText={gettext('Select end date')}
                      selected={dateRange.createdEnd ?? get(config, 'params.created_before', '')}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}
          <div className="col-md-4">
            <label className="control-label text-muted">{gettext('Filter by last changed date')}</label>
            <div className="projects-datepicker">
              <div className="row">
                <div className="col-md-6">
                  <DatePicker
                    autoComplete="off"
                    className="form-control"
                    dateFormat={dateFormat}
                    id="last-changed-start-date-picker"
                    isClearable
                    locale={getLocale(language)}
                    onChange={date => {
                      setStartDate('last_changed', date)
                      if (date) {
                        configActions.updateConfig('params.last_changed_after', formatISO(date, { representation: 'date' }))
                      } else {
                        configActions.deleteConfig('params.last_changed_after')
                      }
                      projectsActions.fetchAllProjects()
                    }}
                    placeholderText={gettext('Select start date')}
                    selected={dateRange.lastChangedStart ?? get(config, 'params.last_changed_after', '')}
                  />
                </div>
                <div className="col-md-6">
                  <DatePicker
                    autoComplete="off"
                    className="form-control"
                    dateFormat={dateFormat}
                    id="last-changed-end-date-picker"
                    isClearable
                    locale={getLocale(language)}
                    onChange={date => {
                      setEndDate('last_changed', date)
                      if (date) {
                        configActions.updateConfig('params.last_changed_before', formatISO(date, { representation: 'date' }))
                      } else {
                        configActions.deleteConfig('params.last_changed_before')
                      }
                      projectsActions.fetchAllProjects()
                    }}
                    placeholderText={gettext('Select end date')}
                    selected={dateRange.lastChangedEnd ?? get(config, 'params.last_changed_before', '')}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

ProjectFilters.propTypes = {
  catalogs: PropTypes.arrayOf(PropTypes.object).isRequired,
  config: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  isManager: PropTypes.bool.isRequired,
  projectsActions: PropTypes.object.isRequired,
}

export default ProjectFilters
