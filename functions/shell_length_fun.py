
def shell_length_gain (shell_length_mm, energy):

    if shell_length_mm < 37:
        sl_weight = 0.8 #changed from 1.8
    elif 37 <= shell_length_mm <= 72:
        sl_weight = 0.7
    elif 72 < shell_length_mm <= 120:
        sl_weight = 0.46
    elif 120 < shell_length_mm <= 200:
        sl_weight = 0.2
    elif 200 < shell_length_mm <= 300:
        sl_weight = 0.06
    elif shell_length_mm > 300:
        sl_weight = 0.01

    return(0.004 * energy * sl_weight) #changed constant from 0.6667

