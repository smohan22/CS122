#HOTEL_PREFERENCE = [{'cost': ['n1','t1','g1']}, {"flights":['n2','t2','g2']}]

glob_storage = None

def final_output(abc):
    global glob_storage
    result1 = {'flights': [[('spirit', 200, 10), ('delta', 30, 40)]], 'buses': 40, 'hotels': [['marriot', 200], ['hayatt', 50]]}
    #glob_storage = abc
    result2 = {'bus': 0, 'uber': 100, 'food': 45, 'hotels': [], 'flights': []}
    return result2

def print_storage(abc):
    return "YAY it works"