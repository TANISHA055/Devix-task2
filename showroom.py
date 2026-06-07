import os
from datetime import datetime

# Database text files as required by the manual
BIKES_FILE = "bikes.txt"
SALES_FILE = "sales.txt"
SERVICE_FILE = "service.txt"

# Admin validation (Requirement: Simple username/password protection)
def admin_login():
    print("\n" + "="*40)
    print("      DEVIX BIKE SHOWROOM LOGIN         ")
    print("="*40)
    username = input("Enter Admin Username: ").strip()
    password = input("Enter Admin Password: ").strip()
    
    if username == "admin" and password == "admin123":
        print("\nLogin Successful! Welcome to the Management Panel.")
        return True
    else:
        print("\nAccess Denied! Invalid Username or Password.")
        return False

# Auto-increment function for Unique Bike ID (Format: DVX-001, DVX-002...)
def generate_bike_id():
    if not os.path.exists(BIKES_FILE):
        return "DVX-001"
    
    with open(BIKES_FILE, "r") as file:
        lines = file.readlines()
        
    if not lines:
        return "DVX-001"
    
    # Extracting ID from the last line of the file
    last_line = lines[-1].strip()
    if last_line:
        try:
            last_id = last_line.split("||")[0]
            last_num = int(last_id.split("-")[1])
            new_num = last_num + 1
            return f"DVX-{new_num:03d}"
        except:
            return "DVX-001"
    return "DVX-001"

# Feature 1: Add new bike details
def add_bike():
    print("\n--- Add New Bike to Showroom Inventory ---")
    bike_id = generate_bike_id()
    print(f"Auto-Generated Bike ID: {bike_id}")
    
    brand = input("Enter Brand Name: ").strip()
    model = input("Enter Model Name: ").strip()
    color = input("Enter Bike Color: ").strip()
    fuel_type = input("Enter Fuel Type (Petrol/EV): ").strip()
    engine_cap = input("Enter Engine Capacity (e.g., 125cc): ").strip()
    year = input("Enter Manufacturing Year: ").strip()
    price = input("Enter Price (INR): ").strip()
    status = "Available"
    
    # Append data into bikes.txt using '||' separator
    bike_data = f"{bike_id}||{brand}||{model}||{color}||{fuel_type}||{engine_cap}||{year}||{price}||{status}\n"
    with open(BIKES_FILE, "a") as file:
        file.write(bike_data)
        
    print(f"\nSuccess: Bike {bike_id} ({brand} {model}) added successfully!")

# Feature 2: View all active showroom inventory
def view_all_bikes():
    print("\n--- Showroom Bike Inventory ---")
    if not os.path.exists(BIKES_FILE):
        print("No inventory logs found.")
        return
        
    with open(BIKES_FILE, "r") as file:
        lines = file.readlines()
        
    found = False
    for line in lines:
        if line.strip():
            parts = line.strip().split("||")
            found = True
            print(f"\nBike ID: {parts[0]} | Brand: {parts[1]} | Model: {parts[2]}")
            print(f"Color: {parts[3]} | Fuel: {parts[4]} | Specs: {parts[5]} | Year: {parts[6]}")
            print(f"Price: Rs. {parts[7]} | Status: {parts[8]}")
            print("-" * 50)
            
    if not found:
        print("Showroom inventory is currently empty.")

# Feature 3: Search vehicle by ID, Model, or Brand
def search_bike():
    print("\n--- Search Inventory Database ---")
    query = input("Enter Bike ID, Brand, or Model to search: ").strip().lower()
    
    if not os.path.exists(BIKES_FILE):
        print("No stock logs available to search.")
        return
        
    with open(BIKES_FILE, "r") as file:
        lines = file.readlines()
        
    found = False
    for line in lines:
        if line.strip():
            parts = line.strip().split("||")
            # Search matching condition
            if query in parts[0].lower() or query in parts[1].lower() or query in parts[2].lower():
                found = True
                print(f"\n[FOUND] ID: {parts[0]} | {parts[1]}…{parts[2]} | Color: {parts[3]}")
                print(f"Price: Rs. {parts[7]} | Current Status: {parts[8]}")
                print("-" * 50)
                
    if not found:
        print("No matching bike records found.")

# Feature 4: Mark Bike as Sold (Removes from available status)
def mark_bike_sold():
    print("\n--- Log Vehicle Retail Sale ---")
    bike_id = input("Enter Bike ID to mark as Sold: ").strip().upper()
    
    if not os.path.exists(BIKES_FILE):
        print("Inventory records not initialized.")
        return
        
    with open(BIKES_FILE, "r") as file:
        lines = file.readlines()
        
    updated_lines = []
    bike_found = False
    sale_record = ""
    
    for line in lines:
        if line.strip():
            parts = line.strip().split("||")
            if parts[0] == bike_id:
                if parts[8] == "Sold":
                    print(f"Action Aborted: Bike {bike_id} is already sold.")
                    return
                parts[8] = "Sold"
                bike_found = True
                sale_record = f"{parts[0]}||{parts[1]} {parts[2]}||{parts[7]}"
                line = "||".join(parts) + "\n"
            updated_lines.append(line)
            
    if bike_found:
        with open(BIKES_FILE, "w") as file:
            file.writelines(updated_lines)
            
        # Log entry to sales.txt
        current_date = datetime.now().strftime("%Y-%m-%d")
        with open(SALES_FILE, "a") as file:
            file.write(f"{sale_record}||{current_date}\n")
            
        print(f"\nSuccess: Vehicle {bike_id} has been marked as Sold.")
    else:
        print(f"Error: Bike ID {bike_id} not found.")

# Feature 5: Service Module - Log a new workshop entry
def log_service_entry():
    print("\n--- Log Workshop Service Entry ---")
    bike_id = input("Enter Bike ID for maintenance entry: ").strip().upper()
    issue = input("Enter Customer Work/Issue Complaint: ").strip()
    cost = input("Enter Estimated Service Cost (INR): ").strip()
    mechanic = input("Enter Assigned Mechanic Name: ").strip()
    service_date = datetime.now().strftime("%Y-%m-%d")
    
    service_data = f"{bike_id}||{issue}||{service_date}||{cost}||{mechanic}\n"
    with open(SERVICE_FILE, "a") as file:
        file.write(service_data)
        
    print(f"\nSuccess: Service job ticket logged for Bike ID {bike_id}.")

# Feature 6: Service Module - View historical data of a bike
def view_service_history():
    print("\n--- Retrieve Vehicle Maintenance Logs ---")
    bike_id = input("Enter Bike ID: ").strip().upper()
    
    if not os.path.exists(SERVICE_FILE):
        print("No service registers found.")
        return
        
    with open(SERVICE_FILE, "r") as file:
        lines = file.readlines()
        
    found = False
    print(f"\nService History Summary for: {bike_id}")
    print("=" * 55)
    for line in lines:
        if line.strip():
            parts = line.strip().split("||")
            if parts[0] == bike_id:
                found = True
                print(f"Date: {parts[2]} | Job Details: {parts[1]}")
                print(f"Bill Cost: Rs. {parts[3]} | Technician: {parts[4]}")
                print("-" * 55)
                
    if not found:
        print("No historical service logs found for this specific ID.")

# Feature 7: Service Module - Generate metric report
def generate_service_report():
    print("\n--- Financial & Workshop Performance Report ---")
    if not os.path.exists(SERVICE_FILE):
        print("No service data found to compute analytics.")
        return
        
    with open(SERVICE_FILE, "r") as file:
        lines = file.readlines()
        
    total_tickets = 0
    gross_revenue = 0.0
    
    for line in lines:
        if line.strip():
            parts = line.strip().split("||")
            total_tickets += 1
            try:
                gross_revenue += float(parts[3])
            except ValueError:
                pass
                
    print(f"Total Service Invoices Closed : {total_tickets}")
    print(f"Total Workshop Revenue Generated: Rs. {gross_revenue:.2f}")

# Main Menu Loop
def main():
    # Admin login verification check at initialization
    if not admin_login():
        return

    while True:
        print("\n" + "="*45)
        print("   BIKE SHOWROOM & SERVICE OPERATIONS   ")
        print("="*45)
        print("1. Add New Bike to Stock")
        print("2. View All Showroom Bikes")
        print("3. Search Bike Records")
        print("4. Register Vehicle Sale (Mark Sold)")
        print("5. Log New Workshop Service Job")
        print("6. Fetch Bike Service History")
        print("7. View Financial Service Report")
        print("8. Exit Operational System")
        print("="*45)
        
        choice = input("Enter Selection (1-8): ").strip()
        
        if choice == "1":
            add_bike()
        elif choice == "2":
            view_all_bikes()
        elif choice == "3":
            search_bike()
        elif choice == "4":
            mark_bike_sold()
        elif choice == "5":
            log_service_entry()
        elif choice == "6":
            view_service_history()
        elif choice == "7":
            generate_service_report()
        elif choice == "8":
            print("\nExiting System Terminal. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please input a digit between 1 and 8.")

if __name__ == "__main__":
    main()