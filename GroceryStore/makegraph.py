import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from pathlib import Path
from GroceryStore.models import Orders
import os
from datetime import timedelta

def calculate_total_revenue_till_now():
    # Load data from CSV file
    df = pd.read_csv("GroceryStore/data/orders.csv")
    total_revenue = df["revenue"].sum()
    return total_revenue

def calculate_total_revenue_this_month():
    # Load data from CSV file and filter by this month
    df = pd.read_csv("GroceryStore/data/orders.csv", parse_dates=["purchase_date"])
    this_month = df[df["purchase_date"].dt.month == pd.Timestamp.now().month]
    total_revenue = this_month["revenue"].sum()
    return total_revenue


def makegraph():
    # Delete the existing 1.png file if it exists
    if os.path.exists('GroceryStore/static/1.png'):
        os.remove('GroceryStore/static/1.png')

    # Export Orders table to a CSV file
    orders = Orders.query.all()
    order_data = []

    for order in orders:
        order_data.append({
            "id": order.id,
            "purchase_date": order.purchase_date,
            "quantity": order.quantity,
            "price_of_item": order.price_of_item,
        })

    df = pd.DataFrame(order_data)

    # Calculate revenue for each order
    df["revenue"] = df["quantity"] * df["price_of_item"]

    # Adjust the path to the instance folder one level up
    csv_filename = Path("GroceryStore/data/orders.csv")
    df.to_csv(csv_filename, index=False)

    # Read the CSV data and create the line chart
    df = pd.read_csv(csv_filename, parse_dates=["purchase_date"])
    df["date"] = df["purchase_date"].dt.date
    daily_revenue = df.groupby("date")["revenue"].sum()  # Sum of daily revenues

    # Create the line chart
    plt.figure(figsize=(10, 6))
    plt.plot(daily_revenue.index, daily_revenue.values, marker='o', linestyle='-')
    plt.xlabel("Date",color='white')
    plt.ylabel("Total Revenue",color='white')
    plt.title("Total Revenue by Date",color='white')

    # Adjust the x-axis scale to start slightly before the minimum date and end slightly after the maximum date
    date_min = min(df["date"]) - timedelta(days=1)  # Subtract 1 day
    date_max = max(df["date"]) + timedelta(days=1)  # Add 1 day
    plt.xlim(date_min, date_max)
    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))  # Format the date as 'YYYY-MM-DD'

    plt.gca().set_facecolor('#000000')  # Set graph background color to black
    plt.gca().spines['bottom'].set_color('white')  # Set border color to white
    plt.gca().spines['top'].set_color('white') 
    plt.gca().spines['right'].set_color('white')
    plt.gca().spines['left'].set_color('white')


    plt.xticks(pd.date_range(start=date_min, end=date_max, freq='D'), rotation=45, color='white')  # Display date labels with rotation
    plt.yticks(color='white')  # Set y-axis text color to white

    # Add these lines to change Y-axis markings color
    plt.gca().tick_params(axis='y', colors='white')  # Set Y-axis tick markings color to white

    # Adjust the path to the instance folder one level up
    chart_filename = Path("GroceryStore/static/1.png")
    plt.savefig(chart_filename,facecolor='#000000', transparent=True)


    # Calculate revenue for each order
    df["revenue"] = df["quantity"] * df["price_of_item"]

    # Calculate total revenue till now
    total_revenue_till_now = df["revenue"].sum()
    print(total_revenue_till_now)

    # Calculate total revenue of this month
    current_month = pd.Timestamp.now().month
    current_year = pd.Timestamp.now().year
    this_month_df = df[(df["purchase_date"].dt.month == current_month) & (df["purchase_date"].dt.year == current_year)]
    total_revenue_this_month = this_month_df["revenue"].sum()
    print(total_revenue_this_month)
    # ... (previous code)
    # Adjust the path to the instance folder one level up
if __name__ == "__main__":
    makegraph()
