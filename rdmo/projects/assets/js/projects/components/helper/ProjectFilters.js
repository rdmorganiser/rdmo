import React from 'react'
import PropTypes from 'prop-types'
import DatePicker from 'react-datepicker'
import { formatISO, set, isValid, parseISO } from 'date-fns'
import { get } from 'lodash'

import { getDateFormat, getLocale, parseDate } from 'rdmo/core/assets/js/utils/date'

import { Link, Select } from 'rdmo/core/assets/js/components'

const ProjectFilters = ({ catalogs, config, configActions, isManager, projectsActions }) => {
  const showFilters = [true, 'true'].includes(get(config, 'showFilters', false))
  const toggleFilters = () => configActions.updateConfig('showFilters', !showFilters)

  const resetAllFilters = () => {
    configActions.deleteConfig('params.catalog')
    configActions.deleteConfig('params.created_after')
    configActions.deleteConfig('params.created_before')
    configActions.deleteConfig('params.last_changed_after')
    configActions.deleteConfig('params.last_changed_before')
    configActions.updateConfig('params.page', '1')
    projectsActions.fetchProjects()
  }

  const catalogOptions = catalogs?.filter(catalog => isManager || catalog.available)
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
    value ? configActions.updateConfig('params.catalog', value) : configActions.deleteConfig('params.catalog')
    projectsActions.fetchProjects()
  }

  const handleDateChange = (type, date) => {
    if (type.endsWith('_after')) {
      if (date) {
        const startOfDayDate = set(date, { hours: 0, minutes: 0, seconds: 0, milliseconds: 0 })
        configActions.updateConfig(`params.${type}`, formatISO(startOfDayDate, { representation: 'complete' }))
      } else {
        configActions.deleteConfig(`params.${type}`)
      }
    } else if (type.endsWith('_before')) {
      if (date) {
        const endOfDayDate = set(date, { hours: 23, minutes: 59, seconds: 59, milliseconds: 999 })
        configActions.updateConfig(`params.${type}`, formatISO(endOfDayDate, { representation: 'complete' }))
      } else {
        configActions.deleteConfig(`params.${type}`)
      }
    }
    projectsActions.fetchProjects()
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
                <label className="control-label text-muted">{gettext('Filter by last changed date')}</label>
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
        </div>
      )}
      <div className="pull-right mt-5">
        {showFilters && !Object.keys(config.params).every(key => ['ordering', 'page', 'search', 'user'].includes(key)) && (
          <Link className="element-link mr-10 mb-10" onClick={resetAllFilters}>
            {gettext('Reset all filters')}
          </Link>
        )}
        <Link className="element-link mb-10" onClick={toggleFilters}>
          {showFilters ? gettext('Hide filters') : gettext('Show filters')}
        </Link>
      </div>
    </>
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
