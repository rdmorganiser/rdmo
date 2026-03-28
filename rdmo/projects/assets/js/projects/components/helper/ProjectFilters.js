import React from 'react'
import PropTypes from 'prop-types'
import DatePicker from 'react-datepicker'
import { useDispatch, useSelector } from 'react-redux'
import { formatISO, set, isValid, parseISO } from 'date-fns'
import { get } from 'lodash'

import { getDateFormat, getLocale, parseDate } from 'rdmo/core/assets/js/utils/date'

import { Select } from 'rdmo/core/assets/js/components'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as projectsActions from '../../actions/projectsActions'

const ProjectFilters = ({ catalogs, isAdminOrSiteManager }) => {
  const dispatch = useDispatch()

  const config = useSelector(state => state.config)
  const roleOptions = useSelector(state => state.roles?.roles) || []

  const showFilters = [true, 'true'].includes(get(config, 'showFilters', false))
  const toggleFilters = () => dispatch(configActions.updateConfig('showFilters', !showFilters))

  const resetAllFilters = () => {
    dispatch(configActions.deleteConfig('params.catalog'))
    dispatch(configActions.deleteConfig('params.role'))
    dispatch(configActions.deleteConfig('params.created_after'))
    dispatch(configActions.deleteConfig('params.created_before'))
    dispatch(configActions.deleteConfig('params.last_changed_after'))
    dispatch(configActions.deleteConfig('params.last_changed_before'))
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
  const handleCatalogFilterChange = (value) => {
    value ? (
      dispatch(configActions.updateConfig('params.catalog', value))
    ) : (
      dispatch(configActions.deleteConfig('params.catalog'))
    )
    dispatch(projectsActions.fetchProjects())
  }

  const selectedRole = get(config, 'params.role', '')
  const handleRoleFilterChange = (value) => {
    value ? (
      dispatch(configActions.updateConfig('params.role', value))
    ) : (
      dispatch(configActions.deleteConfig('params.role'))
    )
    dispatch(projectsActions.fetchProjects())
  }

  const handleDateChange = (type, date) => {
    if (type.endsWith('_after')) {
      if (date) {
        const startOfDayDate = set(date, { hours: 0, minutes: 0, seconds: 0, milliseconds: 0 })
        dispatch(configActions.updateConfig(`params.${type}`, formatISO(startOfDayDate, { representation: 'complete' })))
      } else {
        dispatch(configActions.deleteConfig(`params.${type}`))
      }
    } else if (type.endsWith('_before')) {
      if (date) {
        const endOfDayDate = set(date, { hours: 23, minutes: 59, seconds: 59, milliseconds: 999 })
        dispatch(configActions.updateConfig(`params.${type}`, formatISO(endOfDayDate, { representation: 'complete' })))
      } else {
        dispatch(configActions.deleteConfig(`params.${type}`))
      }
    }
    dispatch(projectsActions.fetchProjects())
  }

  const handleDateChangeRaw = (type, event) => {
    const date = parseDate(event.target.value, type.endsWith('_before'))
    if (isValid(date)) {
      handleDateChange(type, date)
    }
  }

  const getSelected = (type) => {
    const selected = get(config, `params.${type}`)
    return selected ? parseISO(selected) : null
  }

  return (
    <>
      {showFilters && (
        <div className="mt-2">
          <div className="row">
            <div className={`col-md-${isAdminOrSiteManager ? 2 : 4}`}>
              <label className="form-label text-secondary">{gettext('Filter by catalog')}</label>
              <Select
                onChange={handleCatalogFilterChange}
                options={catalogOptions ?? []}
                placeholder={gettext('Select catalog')}
                value={selectedCatalog}
              />
            </div>
            <div className={`col-md-${isAdminOrSiteManager ? 2 : 4}`}>
              <label className="form-label text-secondary">{gettext('Filter by role')}</label>
              <Select
                onChange={handleRoleFilterChange}
                options={roleOptions}
                placeholder={gettext('Select role')}
                value={selectedRole}
              />
            </div>
            {isAdminOrSiteManager && (
              <div className="col-md-4">
                <label className="form-label text-muted">{gettext('Filter by created date')}</label>
                <div className="projects-datepicker">
                  <div className="row">
                    <div className="col-md-6">
                      <DatePicker
                        autoComplete="off"
                        className="form-control"
                        dateFormat={getDateFormat()}
                        id="created-after-date-picker"
                        isClearable
                        locale={getLocale()}
                        onChange={date => handleDateChange('created_after', date)}
                        onChangeRaw={event => handleDateChangeRaw('created_after', event)}
                        placeholderText={gettext('Select start date')}
                        selected={getSelected('created_after')}
                        openToDate={getSelected('created_after')}
                      />
                    </div>
                    <div className="col-md-6">
                      <DatePicker
                        autoComplete="off"
                        className="form-control"
                        dateFormat={getDateFormat()}
                        id="created-before-date-picker"
                        isClearable
                        locale={getLocale()}
                        onChange={date => handleDateChange('created_before', date)}
                        onChangeRaw={event => handleDateChangeRaw('created_before', event)}
                        placeholderText={gettext('Select end date')}
                        selected={getSelected('created_before')}
                        openToDate={getSelected('created_before')}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div className="col-md-4">
              <label className="form-label text-muted">{gettext('Filter by last changed date')}</label>
              <div className="projects-datepicker">
                <div className="row">
                  <div className="col-md-6">
                    <DatePicker
                      autoComplete="off"
                      className="form-control"
                      dateFormat={getDateFormat()}
                      id="last-changed-after-date-picker"
                      isClearable
                      locale={getLocale()}
                      onChange={date => handleDateChange('last_changed_after', date)}
                      onChangeRaw={event => handleDateChangeRaw('last_changed_after', event)}
                      placeholderText={gettext('Select start date')}
                      selected={getSelected('last_changed_after')}
                      openToDate={getSelected('last_changed_after')}
                    />
                  </div>
                  <div className="col-md-6">
                    <DatePicker
                      autoComplete="off"
                      className="form-control"
                      dateFormat={getDateFormat()}
                      id="last-changed-before-date-picker"
                      isClearable
                      locale={getLocale()}
                      onChange={date => handleDateChange('last_changed_before', date)}
                      onChangeRaw={event => handleDateChangeRaw('last_changed_before', event)}
                      placeholderText={gettext('Select end date')}
                      selected={getSelected('last_changed_before')}
                      openToDate={getSelected('last_changed_before')}
                    />
                  </div>
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
        {
          showFilters && !Object.keys(config.params).every(key => ['ordering', 'page', 'search', 'user'].includes(key)) && (
            <button type="button" className="link font-small" onClick={resetAllFilters}>
              <i className="bi bi-x-circle"></i> {gettext('Reset all filters')}
            </button>
          )
        }
      </div>
    </>
  )
}

ProjectFilters.propTypes = {
  catalogs: PropTypes.arrayOf(PropTypes.object).isRequired,
  isAdminOrSiteManager: PropTypes.bool.isRequired,
}

export default ProjectFilters
