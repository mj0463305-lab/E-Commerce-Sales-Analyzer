
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Step 1: Read CSV file
try:
    df = pd.read_csv("orders.csv")

except FileNotFoundError:
    print("Error: orders.csv file not found.")
    sys.exit()

except pd.errors.EmptyDataError:
    print("Error: CSV file is empty.")
    sys.exit()

# Step 2: Check required columns
required_columns = [
    "Order_ID", "Product", "Category", "Quantity", "Price"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("Missing columns:", missing_columns)
    sys.exit()

# Step 3: Remove duplicate rows
df = df.drop_duplicates()

# Step 4: Validate data
valid_rows = []

for index, row in df.iterrows():

    # Check missing Order ID, Product or Category
    if any(
        pd.isna(row[column]) or str(row[column]).strip() == ""
        for column in ["Order_ID", "Product", "Category"]
    ):
        print(f"Row {index + 1} skipped: Missing Order ID, Product or Category")
        continue

    # Convert Quantity and Price into numeric values
    quantity = pd.to_numeric(row["Quantity"], errors="coerce")
    price = pd.to_numeric(row["Price"], errors="coerce")

    # Validate Quantity
    if pd.isna(quantity):
        print(f"Row {index + 1} skipped: Invalid Quantity '{row['Quantity']}'")
    elif quantity <= 0:
        print(f"Row {index + 1} skipped: Quantity must be positive")

    # Validate Price
    if pd.isna(price):
        print(f"Row {index + 1} skipped: Invalid Price '{row['Price']}'")
    elif price <= 0:
        print(f"Row {index + 1} skipped: Price must be positive")

    # Store only valid rows
    if (
        not pd.isna(quantity) and quantity > 0
        and not pd.isna(price) and price > 0
    ):
        valid_rows.append(row)

# Step 5: Convert valid rows into DataFrame
df = pd.DataFrame(valid_rows, columns=df.columns)

df["Quantity"] = pd.to_numeric(df["Quantity"])
df["Price"] = pd.to_numeric(df["Price"])

if df.empty:
    print("No valid records found in the CSV file.")

# Step 6: Calculate Revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# Step 7: Calculate sales summary
total_revenue = df["Revenue"].sum()
total_orders = len(df)
total_units = df["Quantity"].sum()

# Step 8: Product-wise revenue
product_sales = df.groupby("Product")["Revenue"].sum()

# Step 9: Category-wise revenue
category_sales = df.groupby("Category")["Revenue"].sum()

if total_revenue > 0:
    category_percentage = (category_sales / total_revenue) * 100
else:
    category_percentage = category_sales

# Step 10: Find Top 5 products
top_products = product_sales.sort_values(
    ascending=False).head(5)

# Step 11: Create menu
while True:

    print("\n===== E-COMMERCE SALES ANALYZER =====")
    print("1. Sales Summary")
    print("2. Category-wise Revenue")
    print("3. Top 5 Products Chart")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        print("\n----- SALES SUMMARY -----")
        print("Total Revenue:", total_revenue)
        print("Total Orders:", total_orders)
        print("Units Sold:", total_units)

        print("\nTop Products:")
        print(top_products)

        if not product_sales.empty:
            top_product = product_sales.idxmax()
            top_revenue = product_sales.max()

            print("Best Selling Product:",top_product,"(",top_revenue,")")

        else:
            print("No valid products available.")

    elif choice == "2":

        print("\n----- CATEGORY-WISE REVENUE -----")

        if not category_sales.empty:

            print(category_sales)
            print(category_percentage.round(2))


            plt.pie(
                category_sales,
                labels=category_sales.index,
                autopct="%1.1f%%"
            )

            plt.title("Category-wise Revenue")
            plt.show()

        else:
            print("No valid category data available.")

    elif choice == "3":

        if not top_products.empty:

            bars = plt.bar(
                top_products.index,
                top_products.values
            )

            plt.title("Top 5 Products by Revenue")
            plt.xlabel("Products")
            plt.ylabel("Revenue")
            plt.show()

        else:
            print("No valid product data available.")

    elif choice == "4":

        print("Thank you for using E-Commerce Sales Analyzer!")
        break

    else:
        print("Invalid choice! Please try again.")
