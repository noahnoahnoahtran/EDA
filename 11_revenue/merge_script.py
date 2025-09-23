import pandas as pd
import glob
import os


# File path
folder_path = "d:/Code/EDA/11_revenue/datasets"
employee_tenure = "d:/Code/EDA/11_revenue/datasets/employee_tenure.csv"
output_path = "d:/Code/EDA/11_revenue/raw_transactions.csv"

# Read excel files
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
all_data = []

for file in excel_files:
    filename = os.path.basename(file).replace(".xlsx", "")
    employee_id = filename.split("_")[0] if "_" in filename else None
    employee_eng_name = filename.split("_")[1] if "_" in filename else None
    employee_vie_name = filename.split("_")[2] if "_" in filename else None

    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(
            file,
            sheet_name=sheet_name,
            skiprows=1,
            nrows=98,
            usecols="A:S"
            )
        
# Remove empty rows
        df = df[df.iloc[:, 1].notna()]
        df =df.dropna(how="all")

        if not df.empty:
            df["employee_id"] = employee_id
            df["employee_eng_name"] = employee_eng_name
            df["employee_vie_name"] = employee_vie_name
            df["source_file"] = filename
            df["sheet_name"] = sheet_name
            all_data.append(df)

# Merge all data into raw_df
if not all_data:
    raise ValueError("No data in folder.")

raw_df = pd.concat(all_data, ignore_index=True)

# Standardize data type of Payment Date column into datetime
raw_df["Payment Date"] = pd.to_datetime(raw_df["Payment Date"], errors="coerce")

# Read employee_tenure file
emp_tenure = pd.read_csv(employee_tenure, parse_dates=["start_date", "end_date"], dayfirst=True)

# Merge by employee_id
merged = raw_df.merge(emp_tenure[["employee_id", "start_date", "end_date", "employee_team", "employee_position"]], on="employee_id", how="left")

# Set up lookup conditions
mask = (merged["Payment Date"] >= merged["start_date"]) & (merged["Payment Date"] <= merged["end_date"])

# Fill team/position columns only when lookup conditions are satisfied, if not satisfied, then write "None"
merged.loc[~mask, ["employee_team", "employee_position"]] = None

# Remove unnecessary tenure columns
merged = merged.drop(columns=["start_date", "end_date"])

# Export csv file
merged.to_csv(output_path, index=False)
print("CSV created successfully.")