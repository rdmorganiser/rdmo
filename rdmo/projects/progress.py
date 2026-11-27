def compute_navigation(project):
    # compute navigation from answer tree
    answer_tree = project.get_answer_tree(verbose=('section', 'page'))
    if not answer_tree:
        return []

    navigation = []
    for section_node in answer_tree['elements']:
        navigation_section = {
            key: section_node.get(key)
            for key in ['id', 'uri', 'title', 'show', 'first', 'count', 'total']
        }

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
    if not answer_tree:
        return 0, 0

    return answer_tree['count'], answer_tree['total']


def compute_page(project, requested_page, direction):
    answer_tree = project.get_answer_tree()
    if not answer_tree:
        return None

    page_already_found = False

    sections = answer_tree['elements']
    section_iter = sections if direction == 'next' else reversed(sections)
    for section_node in section_iter:
        pages = section_node['elements']
        page_iter = pages if direction == 'next' else reversed(pages)
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
