import csv
import os

# Obtaining soil type as imput from user
soil_type = input("Enter Soil Type (shallow or deep): ")

# Assigning Moisture Holding Capacity(C) and Groundwater fraction(y) values based on Soil type
if soil_type.lower() == "deep":
    C, y = 100, 0.2
elif soil_type.lower() == "shallow":
    C, y = 42, 0.4
print(f'C = {C}, y = {y}')

# Constants
demand = 4

# Initializing soil moisture content to zero
sm = 0

with open('daily_rainfall_jalgaon_chalisgaon_talegaon_2022.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    # Create daily soil water balance file in the output directory
    with open('output/' + str(soil_type.lower())+'_daily_soil_water_balance.csv', 'w', newline='') as new_file:
        fieldnames = ['Day', 'Rainfall in mm', "Runoff + excess runoff in mm", "Crop water uptake in mm",
                      "Soil moisture in mm", "Percolation to groundwater in mm"]

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        n = 1

        for line in csv_reader:

            # Calculating daily soil water balance
            rain = float(line['rain_mm'])

            # Calculation of runoff
            a = 0
            if 0 <= rain < 25:
                a = 0.2
            elif 25 <= rain < 50:
                a = 0.3
            elif 50 <= rain < 75:
                a = 0.4
            elif 75 <= rain < 100:
                a = 0.5
            elif 100 <= rain:
                a = 0.7
            runoff = a * rain

            infiltration = rain - runoff

            # Ensures that excess is always positive
            excess = max(0, infiltration + sm - C)

            total_runoff = excess + runoff

            # Update the soil moisture content
            sm += infiltration - excess

            # Calculate Crop water uptake and update soil moisture content
            # Ensures that uptake is atmost the demand(i.e., 4mm)
            uptake = min(demand, sm)
            sm -= uptake

            # Calculate Percolation to groundwater and update soil moisture content
            gw = y * sm
            sm -= gw

            # Writing to the new file
            new_line = dict()
            new_line['Day'] = n
            new_line['Rainfall in mm'] = rain
            new_line["Runoff + excess runoff in mm"] = total_runoff
            new_line["Crop water uptake in mm"] = uptake
            new_line["Soil moisture in mm"] = sm
            new_line["Percolation to groundwater in mm"] = gw

            n += 1

            csv_writer.writerow(new_line)
