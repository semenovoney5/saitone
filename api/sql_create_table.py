import psycopg2

def createrutor():
    
    conn =  psycopg2.connect('dbname=mydbone user=larry password=qwaszx7cxz host=127.0.0.1')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS rutor(
            id serial PRIMARY KEY,
            title text,
            url text,
            seeds text,
            peers text,
            magnet text,
            created text,
            updated text,
            info_hash text,
            size text)
    ''')

    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usermy(
            id serial PRIMARY KEY,
            wallet text,
            ordermy BOOLEAN NOT NULL,
            symma text,
            username text UNIQUE,
            password text,
            email text UNIQUE
            )''')



    
    
    conn.commit()
    print("table created")



    return conn
createrutor()