

def assert_other_projects_unchanged(other_projects, initial_tasks_state):
    for other_project in other_projects:
        assert set(other_project.tasks.values_list('id', flat=True)) == set(initial_tasks_state[other_project.id])
