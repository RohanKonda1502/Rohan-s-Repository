#To create a program to take order from the customer in hotel and generate bill in windows notificaton and notification for order confirmation and to get confirmation from the customer  whether the order has been delivered or not if not ask which item is missing and to deliver the item and ask rating and review and a password at start to access this program.
import random
import time
from plyer import notification # For Windows notifications

# --- Configuration ---
PASSWORD = "Hotel"  # Change this to your desired password

# --- File Paths ---
MENU_FILE = "menu.txt"
ORDERS_FILE = "orders.txt"

# --- Default Menu (used if menu.txt is empty or doesn't exist) ---
DEFAULT_MENU = {
    "Pizza": 250,
    "Burger": 120,
    "Pasta": 180,
    "Sandwich": 100,
    "Coffee": 60
}
# --- Functions ---
def send_notification(title, message):
    """Function to send a windows notification."""
    print(f"[DEBUG] Trying to send notification: Title='{title}'") # Debug print
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Hotel Order System",
            timeout=20,
            app_icon=r"C:\Users\HP\Downloads\hotel_notification.ico" # You can specify an icon path here if desired
        )
        print("[DEBUG] Notification sent successfully.") # Debug print
    except Exception as e:
        print(f"\n--- !!! NOTIFICATION ERROR !!! ---")
        print(f"Failed to send notification. Please ensure 'plyer' and its dependencies (like 'win10toast-click') are installed.")
        print(f"Error details: {e}")
        print(f"----------------------------------\n")

def get_password():
    """Handles password protection for the system."""
    while True:
        try:
            user_password = input("Enter the password to access the system: ")
            if user_password == PASSWORD:
                print("Access Granted!")
                break
            else:
                print("Incorrect password. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

def load_menu_from_file():
    """Loads the menu from menu.txt. If file doesn't exist, it creates it with default items."""
    try:
        with open(MENU_FILE, 'r') as f:
            menu = {}
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        item_name = parts[0].strip().title()
                        item_price = float(parts[1].strip())
                        menu[item_name] = item_price
            # If the file was empty, the menu will be empty.
            if not menu:
                print(f"'{MENU_FILE}' is empty. Using default menu and recreating file.")
                raise FileNotFoundError # Treat as if file doesn't exist to trigger recreation
            return menu
    except FileNotFoundError:
        print(f"'{MENU_FILE}' not found or is empty. Creating it with default menu items.")
        with open(MENU_FILE, 'w') as f:
            for item, price in DEFAULT_MENU.items():
                f.write(f"{item},{price}\n")
        return DEFAULT_MENU
    except Exception as e:
        print(f"An error occurred while reading the menu file: {e}")
        print("Using default menu as a fallback.")
        return DEFAULT_MENU

def take_order():
    """Displays the menu and takes the customer's order."""
    menu = load_menu_from_file() # Load menu dynamically
    print("\nWelcome to our Hotel!")
    print("Menu:")
    for item, price in menu.items():
        print(f"{item}: ₹{price}")

    order = {}
    while True:
        item_input = input("\nEnter the item you want to order (or type 'done' to finish): ").strip().title()
        if item_input.lower() == 'done':
            if not order:
                print("No items ordered. Exiting program.")
                return None # Return None if no order was placed
            else:
                return order
        
        if item_input in menu:
            while True:
                try:
                    qty = int(input(f"How many {item_input}s would you like? "))
                    if qty > 0:
                        order[item_input] = order.get(item_input, 0) + qty
                        print(f"Added {qty} x {item_input} to your order.")
                        break
                    else:
                        print("Quantity must be a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number for the quantity.")
        else:
            print("Sorry, that item is not on the menu. Please check the spelling.")

def process_and_notify(order):
    """Generates the bill, sends notifications, and handles delivery confirmation."""
    total = 0
    bill_details = "Your Order Summary:\n"
    menu = load_menu_from_file() # Reload menu to ensure current prices for billing

    print("\n--- Your Final Order ---")
    for item, qty in order.items():
        price = menu.get(item, 0) * qty # Use .get() for safety
        print(f"{item} x {qty} = ₹{price}")
        bill_details += f"{item} x {qty} = ₹{price}\n"
        total += price

    print(f"Total Bill: ₹{total}")
    bill_details += f"\nTotal Bill: ₹{total}"

    order_id = random.randint(1000, 9999)
    print(f"\nYour order ID is {order_id}. Please wait while we prepare your order...")

    # --- Save order to file ---
    try:
        with open(ORDERS_FILE, 'a') as f: # 'a' for append mode, creates file if it doesn't exist
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            for item, qty in order.items():
                price_per_item = menu.get(item, 0)
                total_item_price = price_per_item * qty
                # Format: OrderID,ItemName,Quantity,TotalItemPrice,Timestamp
                f.write(f"{order_id},{item},{qty},{total_item_price},{timestamp}\n")
        print(f"Order #{order_id} details saved to '{ORDERS_FILE}'.")
    except IOError as e:
        print(f"Error: Could not save order to '{ORDERS_FILE}': {e}")

    send_notification(
        title=f"Order #{order_id} Confirmed!",
        message="Your order has been placed successfully. We are preparing it now."
    )
    time.sleep(10) # Simulate preparation time

    print("\nYour order is ready for delivery!")
    send_notification(title=f"Bill for Order #{order_id}", message=bill_details)

def confirm_delivery(order):
    """Asks the user to confirm delivery and handles missing items."""
    input("Press Enter when you have received your order...")
    while True:
        confirmation = input("Did you receive your complete order correctly? (yes/no): ").lower().strip()
        if confirmation == "yes":
            print("Thank you for confirming! Enjoy your meal.")
            break
        elif confirmation == "no":
            missing_item = input("We apologize. Which item was missing? ").strip().title()
            if missing_item in order:
                print(f"We are so sorry about the missing {missing_item}. We are sending it to you right away.")
                time.sleep(10) # Simulate re-delivery
                print(f"Your missing item ({missing_item}) has been delivered. Enjoy your complete meal!")
                break
            else:
                print("That item was not part of your original order. Please check again.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def get_feedback():
    """Asks the user for a rating and review."""
    print("\nWe value your feedback!")
    while True:
        try:
            rating = int(input("Please rate your experience (1-5 stars): "))
            if 1 <= rating <= 5:
                review = input("Would you like to leave a review? (optional): ")
                print("\nThank you for your feedback! We hope to see you again soon.")
                break
            else:
                print("Invalid rating. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number for the rating.")

def view_files():
    """Reads and prints the contents of the menu and orders files."""
    print("\n--- Contents of menu.txt ---")
    try:
        with open(MENU_FILE, 'r') as f:
            content = f.read()
            if content.strip():
                print(content)
            else:
                print(f"'{MENU_FILE}' is empty.")
    except FileNotFoundError:
        print(f"'{MENU_FILE}' does not exist yet. It will be created when you first run the order process.")

    print("\n--- Contents of orders.txt ---")
    try:
        with open(ORDERS_FILE, 'r') as f:
            content = f.read()
            if content.strip():
                print(content)
            else:
                print(f"'{ORDERS_FILE}' is empty. No orders have been placed yet.")
    except FileNotFoundError:
        print(f"'{ORDERS_FILE}' does not exist yet. It will be created when the first order is saved.")
    
    input("\nPress Enter to return to the main menu...")

def main():
    """Main function to run the hotel order system."""
    get_password()
    while True:
        print("\n--- Main Menu ---")
        print("1. Place a New Order")
        print("2. View Menu and Order History Files")
        print("3. Exit")
        choice = input("Please select an option (1-3): ").strip()

        if choice == '1':
            order = take_order()
            if order: # Only proceed if an order was actually placed
                process_and_notify(order)
                confirm_delivery(order)
                get_feedback()
        elif choice == '2':
            view_files()
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()