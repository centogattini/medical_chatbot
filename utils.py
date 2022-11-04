#Преобразуем кортеж (1, 0, ...) свободного времени в 9:00, ...
def time_to_text(time):
    res = []
    h = '9'
    m = '00'
    for i in time:
        cur_time = h + ":" + m
        if m == '00':
            m = '30'
        else:
            h = str(int(h)+1)
            m = '00'

        if i == 0:
            res.append(cur_time)

    return res

