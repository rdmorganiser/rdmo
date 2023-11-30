class TasksFactory {

  static createTask(config) {
    return {
      model: 'tasks.task',
      uri_prefix: config.settings.default_uri_prefix,
      sites: config.settings.multisite ? [config.currentSite.id] : [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

}

export default TasksFactory
