def remove_middle_initial(name):
    name = name.split() #['Mark', 'R.', 'Warner']
    return {
        'first_name': name[0],
        'last_name': name[len(name) - 1]
    }