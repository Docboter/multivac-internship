import pandas as pd

packageData = pd.read_csv("package_data.csv")
oeeData = pd.read_csv("oee_data.csv")
errorMessages = pd.read_csv("error_messages_accumulated.csv")

# convert timestamp
packageData["timestamp"] = pd.to_datetime(packageData["timestamp"])
oeeData["timestamp"] = pd.to_datetime(oeeData["timestamp"])

# calculate the total number of packs
packageData["totalPacks"] = packageData["good_packs"] + packageData["reject_packs"]
totalPacks = packageData["totalPacks"].sum()

# output per minute
packageData["cyclesPerMinute"] = 60 / (packageData["timestamp"].diff() / pd.Timedelta(minutes=1))
oeeData["actual_cycles_per_minute"] = oeeData["actual_cycles_per_minute"].fillna(packageData["cyclesPerMinute"])
averageCyclesPerMinute = oeeData["actual_cycles_per_minute"].mean()
targetCyclesPerMinute = 10
cyclesPercent = (averageCyclesPerMinute / targetCyclesPerMinute) * 100

# calculate the 3 most common reasons for downtime
headOfDowntime = errorMessages["code"].value_counts().head(3).reset_index()
headOfDowntime.columns = ["code", "number of errors"]

# Determine the time when most bad packages are produced
packageData["totalRejectPacks"] = packageData["reject_packs"].sum()
maxRejectPacksTimestamp = packageData.loc[packageData["totalRejectPacks"].idxmax(), "timestamp"]

# production prediction
weeklyPacks = packageData.resample("W", on="timestamp").sum()["good_packs"]
averageWeeklyPacks = weeklyPacks.mean()
nextWeeksProjections = averageWeeklyPacks * 4

# Output for point 1
print("Total number of packs:", totalPacks)
print("Actual cycle power per minute: ", int(averageCyclesPerMinute))
print("Achieved cycle performance compared to planned cycle performance: ", int(cyclesPercent), "%")

# Output for point 2
print("Total number of bad packages:", packageData["reject_packs"].sum())
print("Most frequent downtime reasons for bad packaging:")
print(headOfDowntime)
print("Time with the most bad packs:", maxRejectPacksTimestamp)

# Output for point 3
print("Average number of packs per week:", int(averageWeeklyPacks))
print("Forecast pack production for the next 4 weeks:", int(nextWeeksProjections))
