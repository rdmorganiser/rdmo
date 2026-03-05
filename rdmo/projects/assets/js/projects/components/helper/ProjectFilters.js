import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import { get } from 'lodash'
import DatePicker from 'react-datepicker'
import { formatISO, set } from 'date-fns'

import { Select } from 'rdmo/core/assets/js/components'
import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as projectsActions from '../../actions/projectsActions'

import useDatePicker from '../../hooks/useDatePicker'

const ProjectFilters = ({ catalogs, isAdminOrSiteManager }) => {
  const dispatch = useDispatch()

  const config = useSelector(state => state.config)
  const roleOptions = useSelector(state => state.roles?.roles) || []

  const {
    dateRange,
    dateFormat,
    getLocale,
    setStartDate,
    setEndDate
  } = useDatePicker()

  const showFilters = [true, 'true'].includes(get(config, 'showFilters', false))
  const toggleFilters = () => dispatch(configActions.updateConfig('showFilters', !showFilters))

  const resetAllFilters = () => {
    dispatch(configActions.deleteConfig('params.catalog'))
    dispatch(configActions.deleteConfig('params.role'))
    dispatch(configActions.deleteConfig('params.created_after'))
    setStartDate('created', null)
    dispatch(configActions.deleteConfig('params.created_before'))
    setEndDate('created', null)
    dispatch(configActions.deleteConfig('params.last_changed_after'))
    setStartDate('last_changed', null)
    dispatch(configActions.deleteConfig('params.last_changed_before'))
    setEndDate('last_changed', null)
    dispatch(configActions.updateConfig('params.page', '1'))
    dispatch(projectsActions.fetchProjects())
  }

  const catalogOptions = catalogs?.filter(catalog => isAdminOrSiteManager || catalog.available)
    .map(catalog => ({
      value: catalog.id.toString(),
      label: (
        <span className={catalog.available ? '' : 'text-muted'}>
          {catalog.title}
        </span>
      ),
    }))
  const selectedCatalog = get(config, 'params.catalog', '')
  const updateCatalogFilter = (value) => {
    value ? dispatch(configActions.updateConfig('params.catalog', value)) : dispatch(configActions.deleteConfig('params.catalog'))
    dispatch(projectsActions.fetchProjects())
  }

  const selectedRole = get(config, 'params.role', '')
  const updateRoleFilter = (value) => {
    value ? dispatch(configActions.updateConfig('params.role', value)) : dispatch(configActions.deleteConfig('params.role'))
    dispatch(projectsActions.fetchProjects())
  }

  // Abstract function to handle date change
  const handleDateChange = (type, position, date) => {
    if (position === 'start') {
      setStartDate(type, date)
      if (date) {
        const startOfDayDate = set(date, { hours: 0, minutes: 0, seconds: 0, milliseconds: 0 })
        dispatch(configActions.updateConfig(`params.${type}_after`, formatISO(startOfDayDate, { representation: 'complete' })))
      } else {
        dispatch(configActions.deleteConfig(`params.${type}_after`))
      }
    } else if (position === 'end') {
      setEndDate(type, date)
      if (date) {
        const endOfDayDate = set(date, { hours: 23, minutes: 59, seconds: 59, milliseconds: 999 })
        dispatch(configActions.updateConfig(`params.${type}_before`, formatISO(endOfDayDate, { representation: 'complete' })))
      } else {
        dispatch(configActions.deleteConfig(`params.${type}_before`))
      }
    }
    dispatch(projectsActions.fetchProjects())
  }

  return (
    <>
      {showFilters && (
        <div className="mt-2">
          <div className="row">
            <div className={`col-md-${isAdminOrSiteManager ? 2 : 4}`}>
              <label className="form-label text-secondary">{gettext('Filter by catalog')}</label>
              <Select
                onChange={updateCatalogFilter}
                options={catalogOptions ?? []}
                placeholder={gettext('Select catalog')}
                value={selectedCatalog}
              />
            </div>
            <div className={`col-md-${isAdminOrSiteManager ? 2 : 4}`}>
              <label className="form-label text-secondary">{gettext('Filter by role')}</label>
              <Select
                onChange={updateRoleFilter}
                options={roleOptions}
                placeholder={gettext('Select role')}
                value={selectedRole}
              />
            </div>
            {isAdminOrSiteManager && (
              <div className="col-md-4">
                <label className="form-label text-secondary">{gettext('Filter by created date')}</label>
                <div className="row">
                  <div className="col-md-6">
                    <DatePicker
                      autoComplete="off"
                      className="form-control"
                      dateFormat={dateFormat}
                      id="created-start-date-picker"
                      isClearable
                      locale={getLocale()}
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
                      locale={getLocale()}
                      onChange={date => handleDateChange('created', 'end', date)}
                      placeholderText={gettext('Select end date')}
                      selected={dateRange.createdEnd ?? get(config, 'params.created_before', '')}
                    />
                  </div>
                </div>
              </div>
            )}
            <div className="col-md-4">
              <label className="form-label text-secondary">{gettext('Filter by last changed date')}</label>
              <div className="row">
                <div className="col-md-6">
                  <DatePicker
                    autoComplete="off"
                    className="form-control"
                    dateFormat={dateFormat}
                    id="last-changed-start-date-picker"
                    isClearable
                    locale={getLocale()}
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
                    locale={getLocale()}
                    onChange={date => handleDateChange('last_changed', 'end', date)}
                    placeholderText={gettext('Select end date')}
                    selected={dateRange.lastChangedEnd ?? get(config, 'params.last_changed_before', '')}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      <div className="d-flex justify-content-between mt-2">
        <button type="button" className="link font-small" onClick={toggleFilters}>
          <i className="bi bi-filter"></i> {
            showFilters ? gettext('Hide additional filters') : gettext('Show additional filters')
          }
        </button>
        {showFilters && !Object.keys(config.params).every(key => ['ordering', 'page', 'search', 'user'].includes(key)) && (
          <button type="button" className="link font-small" onClick={resetAllFilters}>
            <i className="bi bi-x-circle"></i> {gettext('Reset all filters')}
          </button>
        )}
      </div>
    </>
  )
}

ProjectFilters.propTypes = {
  catalogs: PropTypes.arrayOf(PropTypes.object).isRequired,
  isAdminOrSiteManager: PropTypes.bool.isRequired,
}

export default ProjectFilters
