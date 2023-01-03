# ./models.py
import asyncio
import asyncpg
import datetime

#import psycopg2
import datetime
###################################async##################################################
async def myconn():
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect('postgresql://larry:qwaszx7cxz@127.0.0.1/mydbone',ssl=False)
    
    await conn.execute('''
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
            size text

        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS usermy(
            id serial PRIMARY KEY,
            wallet text,
            ordermy bool,
            symma text,
            username text,
            password text,
            email text
            )''')



    print("table created!!!!!")
    return conn




# async def my_user():
#     # Establish a connection to an existing database named "test"
#     # as a "postgres" user.
#     conn = await asyncpg.connect('postgresql://monty:qwaszx7@localhost/mydbone')
    
#     await conn.execute('''
#         CREATE TABLE IF NOT EXISTS usermy(
#             id serial PRIMARY KEY,
#             wallet text,
#             ordermy text,
#             symma text,
#             username text,
#             password text,
#             email text
#             )''')



#     print(conn)
#     return conn
###################################################################################################
#def myconnmy():
    
    #conn =  psycopg2.connect('dbname=mydbone user=monty password=qwaszx7 host=127.0.0.1')
    #cur = conn.cursor()

    #cur.execute('''
        #CREATE TABLE IF NOT EXISTS rutor(
            #id serial PRIMARY KEY,
            #title text,
            #url text,
            #seeds text,
            #peers text,
            #magnet text,
            #created text,
            #updated text,
            #info_hash text,
            #size text)
    #''')
    ##conn.commit()
    #print("table created")



    #return conn
#asyncio.run(myconn())




# if __name__ == '__main__':
#   loop = asyncio.get_event_loop()
#   loop.run_until_complete(my_user())
#   loop.close()
