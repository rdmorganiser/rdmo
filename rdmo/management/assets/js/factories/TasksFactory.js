class TasksFactory {

  static createTask(config) {
    return {
      model: 'tasks.task',
      uri_prefix: config.settings.default_uri_prefix
    }
  }

}

export default TasksFactory
