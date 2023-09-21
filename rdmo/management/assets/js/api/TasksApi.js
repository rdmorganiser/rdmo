import isNil from 'lodash/isNil'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class TasksApi extends BaseApi {

  static fetchTasks(action) {
    let url = '/api/v1/tasks/tasks/'
    if (action == 'index') url += 'index/'
    return this.get(url)
  }

  static fetchTask(id) {
    return this.get(`/api/v1/tasks/tasks/${id}/`)
  }

  static storeTask(task) {
    if (isNil(task.id)) {
      return this.post('/api/v1/tasks/tasks/', task)
    } else {
      return this.put(`/api/v1/tasks/tasks/${task.id}/`, task)
    }
  }

  static deleteTask(task) {
    return this.delete(`/api/v1/tasks/tasks/${task.id}/`)
  }

}

export default TasksApi
