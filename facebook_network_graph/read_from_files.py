from facebook_network_graph import NetworkGraph


def read_file(file_name):
    data = list()
    with open(file_name, "r", encoding="utf-8") as rfile:
        cont = rfile.readlines()
        length = len(cont) // 2
        for index in range(length):
            name = cont[index * 2].strip()
            fb_id = cont[index * 2 + 1].strip()
            if name:
                data.append((name, fb_id))
    return data


def read_from_files(file_data, path_to_files):

    data = read_file(file_data)
    graph = NetworkGraph(file_name="__larger_base.db")
    graph.clear()
    for name, fb_id in data:
        new_user = graph.add_node(name=name, facebook_id=graph.id_from_url(fb_id))
        graph.read_friends_from_file(new_user, "%s%s.txt" % (path_to_files, name))


def read_from_files2(file_data, path_to_files):

    data = read_file(file_data)
    graph = NetworkGraph(file_name="interested.db")
    graph.clear()
    for name, fb_id in data:
        graph.add_node(name=name, facebook_id=graph.id_from_url(fb_id)).facebook_id
    for name, fb_id in data:
        new_user = graph.findNode(name=name, facebook_id=graph.id_from_url(fb_id))
        graph.read_friends_from_file(new_user, "%s%s.txt" % (path_to_files, name), adding_new=False)

read_from_files2("/home/liepieshov/CourseWork/data/interested.txt",
                 "/home/liepieshov/CourseWork/db_interested/")
