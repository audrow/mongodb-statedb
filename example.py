from mongodb_statedb import StateDb
import pymongo


host = input('What is your MongoDB host? [localhost] >')
port = int(input('What is your MongoDB port? [62345] >'))

statedb = StateDb(
    pymongo.MongoClient(host, port)
)

statedb.create('name', 'Audrow Nash')
statedb.create('age', 28)
statedb.create('email', 'audrow@hey.com')

print(f'Number of keys set: {len(statedb)}')
print(f'Name: {statedb.get("name")}')
print(f'Age: {statedb.get("age")}')
print(f'Email: {statedb.get("age")}')

print('Setting age to 100')
statedb.set('age', 100)
print(f'New age: {statedb.get("age")}')

assert statedb.exists('email')
statedb.delete('email')
assert not statedb.exists('email')

print('Deleting all keys')
statedb.delete_all()
print(f'Number of keys set: {len(statedb)}')
