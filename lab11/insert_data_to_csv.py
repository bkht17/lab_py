import csv
# Data to be written to the CSV file
data = [
    {"user_name": "Arman", "phone_number": "+77471234578"},
    {"user_name": "Beka", "phone_number": "+77054261524"},
    {"user_name": "Dias", "phone_number": "+77025241324"}
]

# Path to the CSV file
csv_file_path = "pb.csv"

# Write data to the CSV file
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    
    # Write header
    writer.writeheader()
    
    # Write data rows
    for row in data:
        writer.writerow(row)