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


    
    parts = filename.split("_")
    eng_name = parts[1] if len(parts) > 1 else None
    vie_name = parts[2] if len(parts) > 2 else None

    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(
            file,
            sheet_name=sheet_name,
            skiprows=1,
            nrows=98,
            usecols="A:S"
            )
        
        df = df[df.iloc[:, 1].notna()]
        
        df =df.dropna(how="all")

        if not df.empty:
            df["employee_id"] = employee_id
            df["employee_eng_name"] = eng_name
            df["employee_vie_name"] = vie_name
            df["employee_position"] = position
            df["employee team"] = team
            df["source_file"] = filename
            df["sheet_name"] = sheet_name
            all_data.append(df)

if all_data:
    raw_df = pd.concat(all_data, ignore_index=True)
    
    raw_df.to_csv(output_path, index=False)
    print("CSV created successfully.")
else:
    print("No data found.")