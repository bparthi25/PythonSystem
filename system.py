import sqlite3 
import os 
from datetime import datetime 
from sqlite3 import Error
from prettytable import PrettyTable
def conect():
    conn = None
    try:
        conn = sqlite3.connect("mydb.db")
    except sqlite3.Error as e:
        print(e)
    return conn
    #   con = sqlite3.connect("mydb.db")
    #   print("connected!") # con.row_factory = sqlite3.Row # print("connection established") return con
    # except Error:
    #     print("Could not connect please check database file")

def disconnect(con, errinp=False):
    if errinp == True:
        print("ID dose not exist !") 
        con.close() 
        exit()
    con.close()
    exit() 
def option1(cursor, ID):
    # Delivery History
    my_table = PrettyTable()
    my_table.field_names = ["Order ID","Order Date","Product Description","Seller Name", "Price", "Qty","Status"]
    cont = cursor.execute("SELECT shopper_orders.order_id,order_date ,product_description,seller_name,'£'|| printf(price,2) AS price, quantity,ordered_products.ordered_product_status FROM shopper_orders INNER JOIN shoppers ON shoppers.shopper_id = shopper_orders.shopper_id INNER JOIN ordered_products ON ordered_products.order_id = shopper_orders.order_id INNER JOIN products ON products.product_id = ordered_products.product_id INNER JOIN sellers ON sellers.seller_id = ordered_products.seller_id WHERE shoppers.shopper_id = 10019 ORDER BY date(order_date) DESC;")
    if not cont:
        print("\nError: The basket is empty.\n")
    else:
        for i in cont :
            my_table.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6]])
    print('\nDelivery History')
    print('---------------')
    print(my_table)
    # exit()
def option2(cursor, ID):
    cont = cursor.execute("SELECT category_description, category_id from categories") 
    print("\n Product Categories") 
    for i, c in cont:
        print (f"{c}. {i}")
    cat = int(input("Enter category id: ")) 
    #os.system("clear") #use cls if on windows
    if cat :
        print("\t\tProducts")
    more = cursor.execute(f"SELECT product_id, product_description  FROM  products where category_id ={cat}")
    data = more.fetchall()
    for i in data:
        print(f"{data.index(i)}-{i[1]}")
    sen = int(input("Product to add : ")) 
    qun = int(input("Input Quantity:")) 
    if sen <= len(data):
        vendors = cursor.execute(f"SELECT sellers.seller_id,seller_name, price FROM product_sellers INNER JOIN sellers ON sellers.seller_id = product_sellers.seller_id WHERE product_id = {i[0]}").fetchall()
    for sl in vendors:
        print(f"{vendors.index(sl)} {sl[1]} {sl[2]}")
    vend = int(input("\t\tSelect Seller : "))
    if vend and vend <= len(vendors):
        query = cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='shopper_baskets'").fetchall()
        print(query)
        cursor.execute(f"INSERT OR IGNORE INTO shopper_baskets VALUES ({query[0][0]},{ID},{str(datetime.now().strftime('%d/%m/%y'))})")
        cursor.execute(f"INSERT OR IGNORE INTO basket_contents VALUES ({query[0][0]},{i[0]}, {sl[0]}, {qun}, {sl[2]})")
        # os.system("clear")
        print("Item added to your basket\n")
    # else:
    #     pass
    else:
        print("Something went wrong ") 
def option3(cursor, ID):
    my_table = PrettyTable()
    my_table.field_names = ["Product Description","Seller Name","Qty", "Price", "Total"]
    cursor.execute(f"SELECT product_description,seller_name,quantity,price FROM basket_contents b JOIN products p ON p.product_id = b.product_id JOIN sellers s ON s.seller_id = b.seller_id")
    det=cursor.fetchall()
    for x in det:
        my_table.add_row([x[0],x[1],x[2],x[3],(x[2]*x[3])])
    print('Basket Contents')
    print('---------------')
    print(my_table)
def option4(cursor,ID):
    cursor.execute(f"SELECT product_description,seller_name,quantity,price FROM basket_contents b JOIN products p ON p.product_id = b.product_id JOIN sellers s ON s.seller_id = b.seller_id")
    basket = cursor.fetchall()

    if not basket:
        print("\nError: The basket is empty.\n")
    else:
        # print("Current basket:", basket)
        # option3(cursor,ID=ID)
        my_table = PrettyTable()
        my_table.field_names = ["Product Description","Seller Name","Qty", "Price", "Total"]
        cursor.execute(f"SELECT product_description,seller_name,quantity,price FROM basket_contents b JOIN products p ON p.product_id = b.product_id JOIN sellers s ON s.seller_id = b.seller_id")
        det=cursor.fetchall()
        total=0
        for x in det:
            my_table.add_row([x[0],x[1],x[2],x[3],(x[2]*x[3])])
            total=total+x[2]*x[3]
        print('\nBasket Contents')
        print('\n---------------')
        print(my_table)
        print('\t\t\t\t\t\t\t\tTotal:', total)
        address=cursor.execute(f"SELECT delivery_address_line_1,delivery_address_line_2,delivery_address_line_3,delivery_post_code FROM shopper_delivery_addresses a JOIN shopper_orders b ON b.delivery_address_id=a.delivery_address_id JOIN shoppers c ON c.shopper_id=b.shopper_id WHERE c.shopper_id={ID}").fetchone()
        if not address:
            enter_address_card_detail()
        else:
            print('\nDelivery Address\n')
            print('1.',address[0],',',address[1],',',address[2],',',address[3],'\n')
            number = input("\nEnter the number against the delivery address you want to choose: ")
            print('\nPayment cards\n\n')
            payment_cards=cursor.execute(f"SELECT DISTINCT card_number FROM shopper_payment_cards a JOIN shopper_orders b ON b.payment_card_id = a.payment_card_id JOIN shoppers c ON c.shopper_id=b.shopper_id WHERE c.shopper_id={ID}")
            count=1
            for row in payment_cards:
                print(count,'. Visa ending in',row[0],'\n')
                count=count+1
            numb = input("\nEnter the number against the payment card you want to choose: ")
            print('Checkout Complete, your order has been placed')
# Enter Shopper address and payment card details and store in SQL
def enter_address_card_detail():
    print("\n As you have not yet placed any orders, you will need to enter a delivery address .\n")
    line1 = input("\nEnter the delivery address line 1: ")
    line2 = input("\nEnter the delivery address line 2: ")
    line3 = input("\nEnter the delivery address line 3: ")
    country = input("\nEnter the delivery country: ")
    postal_code = input("\nEnter the delivery post code: ")
    # PAYMENT CARD
    print("\n As you have not yet placed any orders, you will need to enter your payment card details .\n")
    card_type = input("\nEnter the card type (VISA, MasterCard, AMEX): ")
    card_number = input("\nEnter the 16-digit card number: ")
    print('Checkout Complete, your order has been placed')
def choices():
    con = conect() 
    cursor = con.cursor()
    ID = input("Please input ID : ")
    user = cursor.execute(f"SELECT shopper_first_name from shoppers WHERE shopper_id = {ID}").fetchone()
    [disconnect(con, errinp=True) if user == None 
    else print(f"\nWELCOME {user[0]} \n"),
    print("ORINOCO - SHOPPER MAIN MENU\n___________________________________________________")]
    while True:
        print("\n1. Display your order history") 
        print("2. Add an item to your basket")
        print("3. View Your Basket ")
        print("4. Checkout ") 
        print("5. Exit ") 
        choice = int(input("Select option : ")) 
        # os.system("clear") 
        if (choice == 1):
            option1(cursor, ID)
#       print("option1")
        elif(choice == 2):
            option2(cursor, ID)
        elif(choice == 3):
            option3(cursor, ID)
        elif(choice == 4):
            option4(cursor, ID)
        else:
            disconnect(con)
choices();