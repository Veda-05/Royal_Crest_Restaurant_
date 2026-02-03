import pandas as pd
import os

# Define the Excel file path and sheet name
file_path = "Book1.xlsx"
sheet_name = "Sheet1"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: {file_path} does not exist.")
else:
    # Read the Excel file
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print("Excel file connected successfully.\n")
        print("Contents of Sheet1:")
        print(df)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")

