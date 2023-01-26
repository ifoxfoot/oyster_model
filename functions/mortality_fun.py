
def mort_prob (age, tds, tds_list, tss, tss_list, temp, temp_list, do, do_list):

    #SALINITY
    if age < 365:
        if len(tds_list) >= 7 and all(v < 5 for v in tds_list[-7:]):
            tds_mort = 0.2
        elif tds < 5:
            tds_mort = 0.1
        elif 5 <= tds <= 10:
            tds_mort = 0.005
        elif 10 < tds <= 20:
            tds_mort = 0.001
        elif 20 < tds <= 28:
            tds_mort = 0.001
        elif len(tds_list) >= 7 and all(28 <= v <= 35 for v in tds_list[-7:]):
            tds_mort = 0.02
        elif 28 < tds <= 35:
            tds_mort = 0.01
        elif tds > 35:
            tds_mort = 0.05
    else:
        if len(tds_list) >= 7 and all(v < 3 for v in tds_list[-7:]):
            tds_mort = 0.2
        elif tds < 3:
            tds_mort = 0.1
        elif 3 <= tds <= 10:
            tds_mort = 0.002
        elif 10 < tds <= 20:
            tds_mort = 0.001
        elif 20 < tds <= 28:
            tds_mort = 0.001
        elif len(tds_list) >= 7 and all(28 <= v <= 35 for v in tds_list[-7:]):
            tds_mort = 0.02
        elif 28 < tds <= 35:
            tds_mort = 0.002
        elif tds > 35:
            tds_mort = 0.05

    #TOTAL SUS SOLIDS
    if age < 365:
        if len(tss_list) >= 12 and all(v < 250 for v in tss_list[-12:]):
            tss_mort = 0
        elif tss < 250:
            tss_mort = 0
        elif len(tss_list) >= 12 and all(250 <= v <= 500 for v in tss_list[-12:]):
            tss_mort = 0.002
        elif 250 <= tss <= 500:
            tss_mort = 0.001
        elif len(tss_list) >= 12 and all(500 < v <= 1000 for v in tss_list[-12:]):
            tss_mort  = 0.005
        elif 500 < tss <= 1000:
            tss_mort = 0.002
        elif len(tss_list) >= 12 and all(1000 < v < 1500 for v in tss_list[-12:]):
            tss_mort = 0.015
        elif 1000 < tss <= 1500:
            tss_mort = 0.01
        elif len(tss_list) >= 12 and all(1500 < v <= 3000 for v in tss_list[-12:]):
            tss_mort = 0.1
        elif 1500 < tss <= 3000:
            tss_mort = 0.02
        elif len(tss_list) >= 12 and all(v > 3000 for v in tss_list[-12:]):
            tss_mort = 0.2
        elif tss > 3000:
            tss_mort = 0.15
    else:
        if len(tss_list) >= 12 and all(v < 500 for v in tss_list[-12:]):
            tss_mort = 0
        elif tss < 500:
            tss_mort = 0.001
        elif len(tss_list) >= 12 and all(500 <= v <= 1000 for v in tss_list[-12:]):
            tss_mort = 0.001
        elif 500 <= tss <= 1000:
            tss_mort = 0.0005
        elif len(tss_list) >= 12 and all(1000 < v <= 2000 for v in tss_list[-12:]):
            tss_mort  = 0.0015
        elif 1000 < tss <= 2000:
            tss_mort = 0.0005
        elif len(tss_list) >= 12 and all(2000 < v < 3000 for v in tss_list[-12:]):
            tss_mort = 0.002
        elif 2000 < tss <= 3000:
            tss_mort = 0.0005
        elif len(tss_list) >= 12 and all(3000 < v <= 3500 for v in tss_list[-12:]):
            tss_mort = 0.0025
        elif 3000 < tss <= 3500:
            tss_mort = 0.001
        elif len(tss_list) >= 12 and all(v > 3500 for v in tss_list[-12:]):
            tss_mort = 0.15
        elif tss > 3500:
            tss_mort = 0.1
    
    #TEMPERATURE
    if len(temp_list) >= 7 and all(v <= 4 for v in temp_list[-7:]):
        temp_mort = 0.01
    elif temp <= 4:
        temp_mort = 0.00125
    elif 4 < temp <= 8:
        temp_mort = 0.0005
    elif 8 < temp <= 10:
        temp_mort = 0.0005
    elif 10 < temp <= 20:
        temp_mort = 0.00125
    elif len(temp_list) >= 7 and all(20 < v <= 32 for v in temp_list[-7:]):
        temp_mort = 0.01
    elif 20 < temp <= 32:
        temp_mort = 0.0055
    elif temp > 32:
        temp_mort = 0.015
    
    #DISSOLVED OXYGEN
    if len(do_list) >= 7 and all(v <= 2.4 for v in temp_list[-7:]):
        do_mort = 0.2
    elif do <= 2.4:
        do_mort = 0.1
    elif 2.4 < do <= 4:
        do_mort = 0.0125

    return(tds_mort + tss_mort + temp_mort + do_mort)
