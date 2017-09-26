# NOT USED
# Creating a shelve to store all shots in a persistent file
# shotlist = shelve.open('shotlistest-shelve')


def add_shot_to_shotlist(shotcode, shot):
    '''
    Adds shot to the shotlist shelve
    :param shot:
    :param shotcode:
    :return:
    '''

    shotlist[shotcode] = shot


def print_shotlist():
    for key in shotlist:
        print(key, '=>\n ', shotlist[key], shotlist[key].shotCode, shotlist[key].tcIn)


if __name__ == '__main__':
    print(shotlist)
    print_shotlist()

    # CLose the shelve
    shotlist.close()


################ Ignore ... old ##########################

# shotlist.clear()
