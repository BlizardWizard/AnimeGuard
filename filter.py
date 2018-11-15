# sets up the chat filter list from the chat_filter.txt file
def filter_remove(term):
    filter_file = open("chat_filter.txt", "r")
    filter_list = filter_file.readlines()
    filter_file.close()
    filter_file = open("chat_filter.txt", 'w')
    for element in filter_list:
        if element != term + '\n':
            filter_file.write(element)

def filter_update():
    chat_filter = []
    filter_file = open("chat_filter.txt", "r")
    for line in filter_file.readlines():
        chat_filter.append(line.replace("\n", ''))
    filter_file.close()
    return chat_filter

def isValidFilter(term, filter_bans):
    for element in filter_bans:
        if element in term:
            return False
    return True