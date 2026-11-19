def compute_navigation(project):
    # compute navigation from answer tree
    navigation = []
    answer_tree = project.get_answer_tree(verbose=('section', 'page'))

    for section_node in answer_tree.get('elements', []):
        navigation_section = {
            key: section_node.get(key)
            for key in ['id', 'uri', 'title', 'show', 'first', 'count', 'total']
        }

        navigation_section['pages'] = []

        for page_node in section_node.get('elements', []):
            navigation_page = {
                key: page_node.get(key)
                for key in ['id', 'uri', 'title', 'show', 'count', 'total']
            }
            navigation_section['pages'].append(navigation_page)

        navigation.append(navigation_section)

    return navigation


def compute_progress(project):
    answer_tree = project.get_answer_tree()
    return answer_tree.get('count', 0), answer_tree.get('total', 0)


def compute_page(project, requested_page, direction):
    page_already_found = False

    answer_tree = project.get_answer_tree()

    section_iter = answer_tree.get('elements', []) if direction == 'next' else reversed(answer_tree.get('elements', []))
    for section_node in section_iter:
        page_iter = (
            section_node.get('elements', []) if direction == 'next' else reversed(section_node.get('elements', []))
        )
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
