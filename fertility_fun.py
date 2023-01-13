
import random

def n_babies(age, do, tss, tds, temp):
    
    #SALINITY
    tds_weight = (tds - 8)/5.5

    #TOTAL SUSPENDED SOLIDS
    if tss < 250:
        tss_weight = 1
    elif 250 <= tss <= 300:
        tss_weight = 0.73
    elif 300 < tss <= 450:
        tss_weight = 0.5
    elif 450 < tss < 500:
        tss_weight = 0.4
    elif 500 <= tss <= 550:
        tss_weight = 0.31
    elif 500 < tss< 1000:
        tss_weight = 0.1
    elif 1000 <= tss <= 1500:
        tss_weight = 0.03
    elif tss > 1500:
        tss_weight = 0

    #TEMPERATURE
    if 19 <= temp <= 32:
        temp_weight = 1
    else:
        temp_weight = 0

    #DO
    if do > 2.5:
        do_weight = 1
    else:
        do_weight = 0

    #SEX
    if age < 1095 and random.random() < 0.03:
        female = True
    elif age >= 1095 and random.random() < 0.75:
        female = True
    else:
        female = False

    #FERTILITY
    if female and age >= 365:
        return(int(3 * tds_weight * tss_weight * temp_weight * do_weight))
    else:
        return(0)
        