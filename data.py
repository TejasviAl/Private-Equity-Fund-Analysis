# Project: Private Equity Fund Analysis (By Tejasvi)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Dataset
file_path = "C:\\Users\\shriy\\Desktop\\data\\private_equity_fund_data\\india_private_equity_fund_data.xlsx"
df = pd.read_excel(file_path)

print("✅ Data Loaded Successfully")
print(df.head())

# Cleaning
df.drop_duplicates(inplace=True)
df.ffill(inplace=True)  # forward fill for missing values

# Fund Performance Metrics

# Compute a simple Estimated Return = (Distributions / Capital_Calls) * 100
df["Estimated_Return"] = (df["Distributions"] / df["Capital_Calls"]) * 100

# Group by Fund_ID
fund_performance = df.groupby("Fund_ID").agg({
    "Estimated_Return": ["mean", "std"],
    "NetAssetValue": "last",
    "Investments": "last"
}).reset_index()

fund_performance.columns = ["Fund_ID", "Average_Return", "Volatility", "Latest_NAV", "Latest_Investments"]

# Simple Sharpe Ratio (risk-adjusted return, risk-free = 4%)
risk_free_rate = 0.04
fund_performance["Sharpe_Ratio"] = (
    (fund_performance["Average_Return"]/100 - risk_free_rate) / (fund_performance["Volatility"]/100)
)

print("\n📊 Fund Performance:")
print(fund_performance.head())

# Visualizations

# (a) Risk vs Return (bubble = NAV)
plt.figure(figsize=(8,6))
plt.scatter(fund_performance["Volatility"], fund_performance["Average_Return"],
            s=fund_performance["Latest_NAV"]/1e6, alpha=0.6,
            c=fund_performance["Sharpe_Ratio"], cmap="viridis")
plt.xlabel("Volatility (%)")
plt.ylabel("Average Return (%)")
plt.title("Risk vs Return of Private Equity Funds")
plt.colorbar(label="Sharpe Ratio")
plt.grid(True)
plt.show()

# (b) Fund NAV Trend Over Time
plt.figure(figsize=(10,6))
for fund in df["Fund_ID"].unique():
    subset = df[df["Fund_ID"] == fund]
    plt.plot(subset["Quarter"], subset["NetAssetValue"], label=fund)

plt.xlabel("Quarter")
plt.ylabel("Net Asset Value (NAV)")
plt.title("Fund NAV Growth Over Time")
plt.legend()
plt.grid(True)
plt.show()

# Save Report
report_path = "beginner_fund_report.xlsx"
fund_performance.to_excel(report_path, index=False)

print(f"\n📑 Report generated and saved to {report_path}")


