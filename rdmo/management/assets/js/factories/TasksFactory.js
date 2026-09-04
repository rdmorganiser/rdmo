import { siteId } from 'rdmo/core/assets/js/utils/meta'

class TasksFactory {

  static createTask(config) {
    return {
      model: 'tasks.task',
      uri_prefix: config.settings.default_uri_prefix,
      sites: config.settings.multisite ? [siteId] : [],
      editors: config.settings.multisite ? [siteId] : [],
      task_type: 'task'
    }
  }

}

export default TasksFactory
