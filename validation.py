import csv
# Obtaining soil type as imput from user
soil_type = input("Enter Soil Type (shallow or deep): ")

with open('output/' + str(soil_type.lower())+'_daily_soil_water_balance.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    invariant_1 = True
    sm_prev = 0.0
    rain_sum = 0.0
    total_runoff_sum = 0.0
    uptake_sum = 0.0
    gw_sum = 0.0

    for line in csv_reader:
        rain = float(line['Rainfall in mm'])
        total_runoff = float(line["Runoff + excess runoff in mm"])
        uptake = float(line["Crop water uptake in mm"])
        sm = float(line["Soil moisture in mm"])
        gw = float(line["Percolation to groundwater in mm"])

        invariant_1 &= (rain == round(
            sm - sm_prev + total_runoff + uptake + gw, 10))

        rain_sum += rain
        total_runoff_sum += total_runoff
        uptake_sum += uptake
        gw_sum += gw

        sm_prev = sm

    invariant_2 = (rain_sum == round(
        sm + total_runoff_sum + uptake_sum + gw_sum, 10))

    print(f'Invariant 1 is {"" if invariant_1 else "not "}satisfied')
    print(f'Invariant 2 is {"" if invariant_2 else "not "}satisfied')
