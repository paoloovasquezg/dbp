import psycopg2

import psycopg2

connection = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    password = '123456',
    database = 'test10',
)

cursor = connection.cursor()

cursor.execute('''create table table2(
    id integer primary key,
   completed boolean not null default false
   );
''')

# original
cursor.execute('insert into table2(id,completed) values (1,true);')

# formato tupla
cursor.execute('insert into table2(id,completed) values(%s, %s);',(2,True))

#formato diccionario
cursor.execute('insert into table2(id,completed) values(%(id)s,%(completed)s)',{'id':5,'completed':False})

#formato partido
data = { 
    'id':16,
    'completed': True
}

SQL_INSERT = 'insert into table2(id, completed) values(%(id)s, %(completed)s);'
cursor.execute(SQL_INSERT, data)


cursor.execute('select * from table2;')
result = cursor.fetchall()
print('result: ',result)


connection.commit()
connection.close()
cursor.close()