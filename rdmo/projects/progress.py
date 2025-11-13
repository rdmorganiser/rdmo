def compute_navigation(project, section):
    # compute navigation from answer tree
    navigation = []
    answer_tree = project.get_answer_tree(verbose=('section', 'page'))

    for section_node in answer_tree['elements']:
        navigation_section = {
            key: section_node.get(key)
            for key in ['id', 'uri', 'title', 'show', 'first', 'count', 'total']
        }

        if section and section.id == navigation_section['id']:
            navigation_section['pages'] = []

            for page_node in section_node['elements']:
                navigation_page = {
                    key: page_node.get(key)
                    for key in ['id', 'uri', 'title', 'show', 'count', 'total']
                }
                navigation_section['pages'].append(navigation_page)

        navigation.append(navigation_section)

    return navigation


def compute_progress(project):
    answer_tree = project.get_answer_tree()
    return answer_tree['count'], answer_tree['total']


def compute_page(project, requested_page, direction):
    page_already_found = False

    answer_tree = project.get_answer_tree()

    section_iter = answer_tree['elements'] if direction == 'next' else reversed(answer_tree['elements'])
    for section_node in section_iter:
        page_iter = section_node['elements'] if direction == 'next' else reversed(section_node['elements'])
        for page_node in page_iter:
            if page_node['id'] == requested_page.id:
                # if the page is the requested page, check if it hidden
                if page_node['show']:
                    return page_node['id']
                else:
                    page_already_found = True
            elif page_already_found:
                # if the requested page was already found, check every following page
                if page_node['show']:
                    return page_node['id']
