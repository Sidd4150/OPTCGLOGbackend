import sqlite3
from fastapi.responses import JSONResponse
sql_schema = """
       CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            name TEXT NOT NULL,                   
            img TEXT,                             
            setName TEXT,                             
            price REAL,                           
            groupID INTEGER          
        );"""

def filterDataBase(filter):
    try:
        with sqlite3.connect("cards.db") as conn:
            cursor = conn.cursor()
            if filter == "price":
                sql = "SELECT * FROM cards ORDER BY price DESC"
                cursor.execute(sql)
            elif filter == "priceASC":
                sql = "SELECT * FROM cards ORDER BY price ASC"
                cursor.execute(sql)
            elif filter == "setNameDESC":
                sql = "SELECT * FROM cards ORDER BY setName DESC"
                cursor.execute(sql)
            elif filter == "setNameASC":
                sql = "SELECT * FROM cards ORDER BY setName ASC"
                cursor.execute(sql)
            else:
                print(f"Filter received: {filter}")  # This will show you what value is being passed
                search_name = f"%{filter}%"  # Adding wildcards for partial matching
                cursor.execute("SELECT * FROM cards WHERE name LIKE ?", (search_name,))
                
            
            rows = cursor.fetchall()
            
            cards = []
            for row in rows:
                card = {
                    "id": row[0],
                    "name": row[1],
                    "img": row[2],
                    "setName": row[3],
                    "price": row[4],
                    "groupID": row[5]
                }
                
                cards.append(card)

            return JSONResponse(content={"cards": cards})
            
    except sqlite3.Error as e:
        print(e)

def getCardsDataBase():
    try:
        with sqlite3.connect("cards.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cards")
            rows = cursor.fetchall()

            if not rows:
                print("No cards found in database.")
            
            cards = []
            for row in rows:
                card = {
                    "id": row[0],
                    "name": row[1],
                    "img": row[2],
                    "setName": row[3],
                    "price": row[4],
                    "groupID": row[5]
                }
                
                cards.append(card)

            return JSONResponse(content={"cards": cards})

    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Log database errors
        return JSONResponse(status_code=500, content={"message": f"Error fetching data: {e}"})

    except Exception as e:
        print(f"Unexpected error: {e}")  # Log other errors
        return JSONResponse(status_code=500, content={"message": f"Unexpected error: {e}"})

def addtoDataBase(data):
    try:
        with sqlite3.connect("cards.db") as conn:
            cursor = conn.cursor()
            sql = ''' INSERT INTO cards(name,img,setName,price,groupID)
              VALUES(?,?,?,?,?) '''
            
            cursor.execute(
                sql, 
                (
                    data["name"],
                    data["img"], 
                    data["setName"],
                    data["price"],
                    data["groupID"],
                  
                  )
                ) 
        
            conn.commit()   #commit changes
            print("added data")
    except sqlite3.Error as e:
        print(e)


def createDataBase():
    try:
        with sqlite3.connect("cards.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS cards")
            cursor.execute(sql_schema)  #create table if not exist
        
            conn.commit()   #commit changes
            print("table created")
    except sqlite3.Error as e:
        print(e)

    
