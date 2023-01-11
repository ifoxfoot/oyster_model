

#DISSOLVED OXYGEN

def do_juvi (do):
    if do >= 2.4:
        return(1.0)
    elif 0.5 <= do < 2.4:
        return(0.5)
    elif do < 0.5:
        return(0.0)
 

def do_adult (do):
    if do >= 2.4:
        return(1.0)
    elif 0.5 <= do < 2.4:
        return(0.75)
    elif do < 0.5:
        return(0.25)

#SALINITY

def tds_juvi (tds, tds_list):
    if len(tds_list) > 7 and all(v < 12 for v in tds_list[-7:]):
        return(0.8)
    elif tds < 12:
        return(0.9)
    elif 12 <= tds <= 27:
        return(1.0)
    elif tds > 27:
        return(0.5)

def tds_adult (tds, tds_list):
    if len(tds_list) >= 7 and all(v < 12 for v in tds_list[-7:]):
        return(0.9)
    elif tds < 12:
        return(0.95)
    elif 12 <= tds <= 35:
        return(1.0)
    elif tds > 35:
        return(0.5)


#TOTAL SUSPENDED SOLIDS

def tss_juvi (tss, tss_list):
    if tss < 250:
        return(1.0)
    elif len(tss_list) >= 14 and all(250 < v <= 500 for v in tss_list[-14:]):
        return(0.8)
    elif 250 < tss <= 500: 
        return(0.9)
    elif 500 < tss <= 2000:
        return(0.5)
    elif len(tss_list) >= 14 and all(v > 2000 for v in tss_list[-14:]):
        return(0.1)
    elif tss > 2000:
        return(0.25)

def tss_adult (tss, tss_list):
    if tss < 500:
        return(1.0)
    elif len(tss_list) >= 14 and all(500 < v <= 1500 for v in tss_list[-14:]):
        return(0.8)
    elif 500 < tss <= 1500: 
        return(0.9)
    elif 1500 < tss <= 3000:
        return(0.5)
    elif len(tss_list) >= 14 and all(v > 3000 for v in tss_list[-14:]):
        return(0.1)
    elif tss > 3000:
        return(0.25)

#TEMPERATURE

def temp_juvi (temp, temp_list):
    if len(temp_list) >= 7 and all(v <= 5 for v in temp_list[-7:]):
        return(0.9)
    elif temp <= 5:
        return(0.95)
    elif 5 < temp <= 32:
        return(1)
    elif temp > 32:
        return(0.5)

def temp_adult (temp, temp_list):
    if len(temp_list) >= 7 and all(v <= 5 for v in temp_list[-7:]):
        return(0.9)
    elif temp <= 5:
        return(0.95)
    elif 5 < temp <= 32:
        return(1)
    elif temp > 32:
        return(0.75)