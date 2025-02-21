import sqlite3
import yfinance as yf

# Connect to SQLite Database
conn = sqlite3.connect("portfolio.db")
cursor = conn.cursor()

# Create Table for Stocks
cursor.execute('''CREATE TABLE IF NOT EXISTS stocks 
                  (symbol TEXT PRIMARY KEY, quantity INTEGER, price REAL)''')
conn.commit()

# Function to fetch stock price
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"][0]
        return price
    except:
        print("Error fetching stock data. Please check the symbol.")
        return None

# Function to add stock
def add_stock():
    symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").upper()
    quantity = int(input("Enter quantity: "))
    price = get_stock_price(symbol)
    
    if price:
        cursor.execute("INSERT OR REPLACE INTO stocks (symbol, quantity, price) VALUES (?, ?, ?)", 
                       (symbol, quantity, price))
        conn.commit()
        print(f"{symbol} added to portfolio at ${price:.2f} per share.")

# Function to view portfolio
def view_portfolio():
    cursor.execute("SELECT * FROM stocks")
    stocks = cursor.fetchall()
    
    if not stocks:
        print("Your portfolio is empty.")
        return
    
    print("\nYour Stock Portfolio:")
    for stock in stocks:
        print(f"📈 {stock[0]} | Quantity: {stock[1]} | Last Price: ${stock[2]:.2f}")
    print("\n")

# Function to remove stock
def remove_stock():
    symbol = input("Enter stock symbol to remove: ").upper()
    cursor.execute("DELETE FROM stocks WHERE symbol = ?", (symbol,))
    conn.commit()
    print(f"{symbol} removed from portfolio.")

# Function to update stock prices
def update_prices():
    cursor.execute("SELECT symbol FROM stocks")
    stocks = cursor.fetchall()
    
    for stock in stocks:
        symbol = stock[0]
        new_price = get_stock_price(symbol)
        if new_price:
            cursor.execute("UPDATE stocks SET price = ? WHERE symbol = ?", (new_price, symbol))
    
    conn.commit()
    print("Stock prices updated successfully.")

# Main Menu
def main():
    while True:
        print("\n📊 STOCK PORTFOLIO TRACKER 📊")
        print("1. Add Stock")
        print("2. View Portfolio")
        print("3. Remove Stock")
        print("4. Update Stock Prices")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_stock()
        elif choice == "2":
            view_portfolio()
        elif choice == "3":
            remove_stock()
        elif choice == "4":
            update_prices()
        elif choice == "5":
            print("Exiting... Have a great day! 🚀")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the Program
if __name__ == "__main__":
    main()
 