
def energy_gain(age, do, tds, tds_list, tss, tss_list, temp, temp_list):
    
    #JUVI ENERGY INPUTS
    if age < 365:
        
        #DISSOLVED OXYGEN
        if do >= 2.4:
            do_energy = 1.0
        elif 0.5 <= do < 2.4:
            do_energy = 0.5
        elif do < 0.5:
            do_energy = 0.0

        #SALINITY
        if len(tds_list) >= 7 and all(v < 12 for v in tds_list[-7:]):
            tds_energy = 0.8
        elif tds < 12:
            tds_energy = 0.9
        elif 12 <= tds <= 27:
            tds_energy = 1.0
        elif tds > 27:
            tds_energy = 0.5

        #TOTAL SUSPENDED SOLIDS
        if tss <= 250:
            tss_energy = 1.0
        elif len(tss_list) >= 14 and all(250 < v <= 500 for v in tss_list[-14:]):
            tss_energy = 0.8
        elif 250 < tss <= 500: 
            tss_energy = 0.9
        elif 500 < tss <= 2000:
            tss_energy = 0.5
        elif len(tss_list) >= 14 and all(v > 2000 for v in tss_list[-14:]):
            tss_energy = 0.1
        elif tss > 2000:
            tss_energy = 0.25

        #TEMPERATURE
        if len(temp_list) >= 7 and all(v <= 5 for v in temp_list[-7:]):
            temp_energy = 0.9
        elif temp <= 5:
            temp_energy = 0.95
        elif 5 < temp <= 32:
            temp_energy = 1.0
        elif temp > 32:
            temp_energy = 0.5

    #ADULT ENERGY INPUTS
    else:

        #DISSOLVED OXYGEN
        if do >= 2.4:
            do_energy = 1.0
        elif 0.5 <= do < 2.4:
            do_energy = 0.75
        elif do < 0.5:
            do_energy = 0.25

        #SALINITY
        if len(tds_list) >= 7 and all(v < 12 for v in tds_list[-7:]):
            tds_energy = 0.9
        elif tds < 12:
            tds_energy = 0.95
        elif 12 <= tds <= 35:
            tds_energy = 1.0
        elif tds > 35:
            tds_energy = 0.5

        #TOTAL SUSPENDED SOLIDS
        if tss <= 500:
            tss_energy = 1.0
        elif len(tss_list) >= 14 and all(500 < v <= 1500 for v in tss_list[-14:]):
            tss_energy = 0.8
        elif 500 < tss <= 1500: 
            tss_energy = 0.9
        elif 1500 < tss <= 3000:
            tss_energy = 0.5
        elif len(tss_list) >= 14 and all(v > 3000 for v in tss_list[-14:]):
            tss_energy = 0.1
        elif tss > 3000:
            tss_energy = 0.25

        #TEMPERATURE
        if len(temp_list) >= 7 and all(v <= 5 for v in temp_list[-7:]):
            temp_energy = 0.9
        elif temp <= 5:
            temp_energy = 0.95
        elif 5 < temp <= 32:
            temp_energy = 1.0
        elif temp > 32:
            temp_energy = 0.75

    #return weighted energy
    return(2.8 * do_energy * tds_energy * tss_energy * temp_energy)

