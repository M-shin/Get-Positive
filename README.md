# Get-Positive
A review analysis tool for small business customers 

# MongoDB setup
To setup MongoDB on a Mac

1. Install MongoDB
  1. Install Brew
  2. Run the command 'brew install mongodb'

2. Install pymongo
  1. Install Pip with the command 'sudo easy_install pip'
  2. Install pymongo with the command 'pip install pymongo'

3. Run MongoDB
  1. add a /data/db directory with the command 'mkdir /data/db'
  2. run mongod on a terminal with the command 'mongod'
  3. (optional) open mongo shell with the command 'mongo'

4. Populate Database
  1. run mockDB.py with 'python mockDB.py'
  2. switch to the mockDB database with the command 'use mockDB'
  3. (optional) use mongo shell to examine db contents with 'db.reviews.find()'
