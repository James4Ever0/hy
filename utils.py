def my_min(a,b, index=0):
    if index ==0:
        if a == b:
            return a
    if a[index] < b[index]:
        return a
    elif a[index] > b[index]:
        return b
    else:
        return my_min(a,b, index=index+1)

def my_max(a,b):
    if a == b:
        return a
    minval = my_min(a,b)
    if minval == a:
        return b
    return a

def my_a_greater_than_b(a,b): # these are tuples.
    if a == b:
        return False
    maxval = my_max(a,b)
    signal = maxval == a
    return signal

def my_a_within_b(a,b):
    if a == b:
        return False
    a_s, a_e = a['start'], a['end']
    b_s, b_e = b['start'], b['end']
    if a_s == b_s or a_e == b_e: return False
    c_s, c_e = my_min(a_s, b_s), my_max(a_e,b_e)
    signal = (c_s == a_s) and (c_e == a_e)
    return signal