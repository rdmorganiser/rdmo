import React, { useEffect } from 'react'
import { useQuery } from 'react-query'
import PropTypes from 'prop-types'

import { get } from 'lodash'
import DatePicker from 'react-datepicker'
import { formatISO, set  } from 'date-fns'

import { Select } from 'rdmo/core/assets/js/components'
import useDatePicker from '../../hooks/useDatePicker'
import { language } from 'rdmo/core/assets/js/utils'

import ProjectsApi from '../../api/ProjectsApi'

const ProjectFilters = ({ config, configActions, isManager, projectsActions }) => {
  const {
    dateRange,
    dateFormat,
    getLocale,
    setStartDate,
    setEndDate
  } = useDatePicker()

  const fetchCatalogs = () => ProjectsApi.fetchCatalogs()

  const { data } = useQuery('catalogs', fetchCatalogs)
  const catalogOptions = data?.map(catalog => ({ value: catalog.id.toString(), label: catalog.title }))
  const selectedCatalog = get(config, 'params.catalog', '')

  const updateCatalogFilter = (value) => {
    value ? configActions.updateConfig('params.catalog', value) : configActions.deleteConfig('params.catalog')
    projectsActions.fetchAllProjects()
  }

  useEffect(() => {
    if (selectedCatalog && catalogOptions) {
      const existsInOptions = catalogOptions.some(option => option.value === selectedCatalog)
      if (!existsInOptions) {
        updateCatalogFilter()
      }
    }
  }, [selectedCatalog, catalogOptions])

  const handleDateChange = (type, position, date) => {
    if (position === 'start') {
      setStartDate(type, date)
      if (date) {
        const startOfDayDate = set(date, { hours: 0, minutes: 0, seconds: 0, milliseconds: 0 })
        configActions.updateConfig(`params.${type}_after`, formatISO(startOfDayDate, { representation: 'complete' }))
      } else {
        configActions.deleteConfig(`params.${type}_after`)
      }
    } else if (position === 'end') {
      setEndDate(type, date)
      if (date) {
        const endOfDayDate = set(date, { hours: 23, minutes: 59, seconds: 59, milliseconds: 999 })
        configActions.updateConfig(`params.${type}_before`, formatISO(endOfDayDate, { representation: 'complete' }))
      } else {
        configActions.deleteConfig(`params.${type}_before`)
      }
    }
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
                      onChange={date => handleDateChange('created', 'start', date)}
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
                      onChange={date => handleDateChange('created', 'end', date)}
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
                    onChange={date => handleDateChange('last_changed', 'start', date)}
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
                    onChange={date => handleDateChange('last_changed', 'end', date)}
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
  config: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  isManager: PropTypes.bool.isRequired,
  projectsActions: PropTypes.object.isRequired,
}

export default ProjectFilters
