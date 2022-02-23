from flask import Flask, request, render_template_string, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST','GET'])
@cross_origin(supports_credentials=True)

def index():
    Load_Energy = []
    sent_data = request.get_json()
    print(sent_data[1])
    for row in sent_data[0]:
        Load_Energy.append(row['PV Energy'] + row['Utility Import Energy'] - row['Utility Export Energy'])
    # print(Load_Energy)

    a = 1
    day = 1
    Total_day = []
    each_30 = []
    total_day = []

    for i in Load_Energy:
        each_30.append(i)
        if a == 48:
            total_day.append(each_30)
            each_30 = []
            Total_day.append("Day" + str(day))
            a = 0
            day += 1
        a += 1


    highest_day = []  # Hightest Value in Each 30 minutes in day
    i = 0
    while len(total_day) > i:
        highest_day.append(max(total_day[i]))
        i += 1


    MD_Reduction = 10

    MD = []
    i = 0
    while len(highest_day) > i:
        MD.append(highest_day[i] * 2)
        i += 1


    Total = 100 - MD_Reduction
    MD_Threshold = []

    i = 0
    while len(MD) > i:
        MD_Threshold.append(MD[i] * Total / 100)
        i += 1
    # print("MD Threshold: " + str(MD_Threshold) + "(kW)")

    More_than_Energy = []  # kWh
    i = 0
    while len(MD) > i:
        More_than_Energy.append(MD_Threshold[i] / 2)
        i += 1
    # print(More_than_Energy)

    Battery_Discharged_Energy_Each_Day = []
    Battery_Discharged_30 = []
    b = 0
    while len(total_day) > b:
        Battery_Discharged_Energy_Each_30 = []
        for i in total_day[b]:
            if i > More_than_Energy[b]:
                Battery_Discharged_Energy_Each_30.append(i - More_than_Energy[b])
        b += 1
        Battery_Discharged_30.append(Battery_Discharged_Energy_Each_30)
        Battery_Discharged_Energy_Each_Day.append(sum(Battery_Discharged_Energy_Each_30))
    Battery_Discharged_Energy = Battery_Discharged_Energy_Each_Day

    Battery_capacity = []

    i = 0
    while len(Battery_Discharged_Energy) > i:
        Battery_capacity.append(Battery_Discharged_Energy[i] / 0.9)
        i += 1

    perk_period_price = 45.1  # For each kilowatt of maximum demand per month during the peak period
    MD_Charges = []  # RM
    i = 0
    while len(MD) > i:
        MD_Charges.append(MD[i] * perk_period_price)
        i += 1

    Each_Battery_kWh_Cost = int(sent_data[1])  # USD/kWh
    RM = 4.2  # 1USD = RM4.2
    Battery_Cost = []

    i = 0
    while len(MD) > i:
        Battery_Cost.append(Battery_capacity[i] * Each_Battery_kWh_Cost * RM)
        i += 1

    Each_Inverter_kW_Cost = int(sent_data[2])  # USD/kW
    Inverter_Cost = []
    b = 0

    while len(Battery_Discharged_Energy_Each_Day) > b:
        Inverter_Cost_Each_30 = []

        if Battery_Discharged_30[b] == []:
            Inverter_Cost_Each_30.append(0 * 1.5 * Each_Inverter_kW_Cost * RM)
        else:
            Inverter_Cost_Each_30.append(max(Battery_Discharged_30[b]) * 1.5 * Each_Inverter_kW_Cost * RM * 2)
        b += 1
        Inverter_Cost.append(sum(Inverter_Cost_Each_30))

    Investment = []

    i = 0
    while len(Inverter_Cost) > i:
        Investment.append((Battery_Cost[i] + Inverter_Cost[i]))
        i += 1

    MD_Saving_Per_Year = []

    i = 0
    while len(Inverter_Cost) > i:
        MD_Saving_Per_Year.append(MD_Charges[i] * MD_Reduction / 100 * 12)
        i += 1

    Save = 0.141  # 0.141 is the price difference between the peak and off peak tariff, we will basically save 0.141 per kWh
    Day = 365  # 1 Year How many day?
    Energy_Trading_profit_per_year = []

    i = 0
    while len(Battery_Discharged_Energy) > i:
        Energy_Trading_profit_per_year.append(Battery_Discharged_Energy[i] * Save * Day)
        i += 1

    Total_Saving = []

    i = 0
    while len(MD_Saving_Per_Year) > i:
        Total_Saving.append(MD_Saving_Per_Year[i] + Energy_Trading_profit_per_year[i])
        i += 1

    ROI = []
    i = 0
    while len(Investment) > i:
        ROI.append(round(Investment[i] / Total_Saving[i], 2))
        i += 1
    print(ROI)

    MD_Saving_Per_Day = []

    i = 0
    while len(Inverter_Cost) > i:
        MD_Saving_Per_Day.append(MD_Charges[i] * MD_Reduction / 100 /31)
        i += 1

    Energy_Trading_profit_per_day = []
    i = 0
    while len(Battery_Discharged_Energy) > i:
        Energy_Trading_profit_per_day.append(Battery_Discharged_Energy[i] * Save)
        i += 1

    Total_Saving_Day = []
    i = 0
    while len(MD_Saving_Per_Year) > i:
        Total_Saving_Day.append(MD_Saving_Per_Day[i] + Energy_Trading_profit_per_day[i])
        i += 1

    return ({'roi':ROI, 'day': Total_day, 'saving_per_day': Total_Saving_Day})

if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/", methods=['POST','GET'])
# @cross_origin(supports_credentials=True)
#
# def index():
#     Load_Energy = []
#     sent_data = request.get_json()
#     for row in sent_data:
#         Load_Energy.append(row['PV Energy'] + row['Utility Import Energy'] - row['Utility Export Energy'])
#     # print(Load_Energy)
#     print(max(Load_Energy))
#
#     MD_Reduction = 10
#
#     MD = max(Load_Energy) * 2
#
#     Total = 100 - MD_Reduction
#     MD_Threshold = MD * Total / 100
#
#     Threshold = MD_Threshold / 2  # kWh
#
#     Battery_Discharged_Energy_Each_30 = []
#
#     for i in Load_Energy:
#         if i > Threshold:
#             Battery_Discharged_Energy_Each_30.append(i - Threshold)
#
#     Battery_Discharged_Energy = sum(Battery_Discharged_Energy_Each_30)
#
#     BESS_Capacity = Battery_Discharged_Energy / 0.9
#
#     Each_Battery_kWh_Cost = 305 #USD/kWh
#     Battery_Cost = Each_Battery_kWh_Cost * 4.2 * BESS_Capacity
#
#     Each_Inverter_kW_Cost = 90 #USD/kW
#     Inverter_Cost = max(Battery_Discharged_Energy_Each_30) * 1.5 * Each_Inverter_kW_Cost * 4.2 * 2
#
#     Investment = Battery_Cost + Inverter_Cost
#     print("Investment: RM" + str(Investment))
#
#     perk_period_price = 45.1  # For each kilowatt of maximum demand per month during the peak period
#     MD_Charges = MD * perk_period_price  # RM
#     print("MD Charges RM" + str(MD_Charges))
#
#     Month = 12  # 1 Year How many month
#     MD_Saving_Per_Year = MD_Charges * MD_Reduction / 100 * Month
#     MD_Saving_Per_Year = round(MD_Saving_Per_Year, 2)
#     print("MD Saving per year: RM" + str(MD_Saving_Per_Year))
#
#     Save = 0.141  # 0.141 is the price difference between the peak and off peak tariff, we will basically save 0.141 per kWh
#     Day = 365  # 1 Year How many day?
#     Energy_Trading_profit_per_year = Battery_Discharged_Energy * Save * Day
#     Energy_Trading_profit_per_year = round(Energy_Trading_profit_per_year, 2)
#     print("Energy Trading profit per year: RM" + str(Energy_Trading_profit_per_year))
#
#     Total_Saving = MD_Saving_Per_Year + Energy_Trading_profit_per_year
#     Total_Saving = round(Total_Saving, 2)
#     print("Total Saving: RM" + str(Total_Saving))
#
#     ROI = Investment / Total_Saving
#     ROI = round(ROI, 2)
#     print(ROI)
#
#     return ({'yes':'wong'})