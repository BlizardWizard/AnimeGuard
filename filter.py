# sets up the chat filter list from the chat_filter.txt file
def filter_remove(term, serverid):
    targetFile = "servers/" + serverid + "/chat_filter.txt"
    filter_file = open(targetFile, "r")
    filter_list = filter_file.readlines()
    filter_file.close()
    filter_file = open(targetFile, 'w')
    for element in filter_list:
        if element != term + '\n':
            filter_file.write(element)


def get_filter(serverid):
    chat_filter = []
    filter_file = open("servers/" + serverid + "/chat_filter.txt", "r+")
    for line in filter_file.readlines():
        chat_filter.append(line.replace("\n", ''))
    filter_file.close()
    return chat_filter


def add_filter(term, serverid):
    filter_file = open("servers/" + serverid + "/chat_filter.txt", 'a')
    filter_file.write(term + "\n")
    filter_file.close()


def isValidFilter(term, filter_bans):
    for element in filter_bans:
        if element in term:
            return False
    return True
