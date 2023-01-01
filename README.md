# sanic plus rutor parser plus bitcon pay
Платный просмотр фильмов оплата в bitcoin для вашего сайта.



Создание вертуального акружения:


python3 -m venv venv


source venv/bin/activate


pip install -r requirements.txt


Создание таблицы postgres:

В файле sql_create_table.py и models.py

прописываем название логин и пароль базы данных postgres

python3 sql_create_table.py


Запуск парсера:

python3 rutor_parser.py

Если запускаете парсер первый раз 

раскоментиуйте две строки вфайле wildres.py

create и закоментируйте update

####################created#####################
# cur.execute('''INSERT INTO rutor(title,url,seeds,peers,magnet,created,updated,info_hash,size) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],item['created'],item['created'],item['info_hash'],item['size']))
# conn.commit()
####################updated#####################

cur.execute('''UPDATE  rutor SET title=%s,url=%s,seeds=%s,peers=%s,magnet=%s,updated=%s,info_hash=%s,size=%s WHERE id = %s''',(item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],created,item['info_hash'],item['size'],res))
conn.commit()
####################################################

create записывает данные в базу а update обновляет все данные в базе.# saitone
