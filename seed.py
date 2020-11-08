from nessie import Nessie

def reset_data():

  nessie = Nessie()
  
  nessie.delete_all_data()
  
  customer = {
    "first_name": "Kim",
    "last_name": "Wexler",
    "address": {
      "street_number": "123",
      "street_name": "Elm Street",
      "city": "Baltimore",
      "state": "MD",
      "zip": "12041"
    }
  }
  
  resp = nessie.post('/Customers', customer)
  
  customer_id = resp['objectCreated']['_id']
  print('Created customer ' + customer_id)
  
  account = {
    "type": "Checking",
    "nickname": "Checking",
    "rewards": 0,
    "balance": 0
  }
  
  resp = nessie.post('/customers/' + customer_id + '/accounts', account)
  
  account_id = resp['objectCreated']['_id']
  print('Created account ' + account_id)
  
  deposits = [
    ('2020-08-31', 'Paycheck', 750),
    ('2020-08-20', 'Won a bet', 10), 
    ('2020-07-31', 'Birthday Money', 750), 
    ('2020-06-25', 'Won a bet', 10), 
    ('2020-06-12', 'IM RICH', 100000), 
    ('2020-06-10', 'Paycheck', 1000), 
    ('2020-05-10', 'Paycheck', 1000), 
    ('2020-04-10', 'Paycheck', 1000), 
    ('2020-03-10', 'Paycheck', 1000), 
    ('2020-03-02', 'Despositing 500(allowance)', 500), 
    ('2020-02-12', 'Depositing 250', 250), 
    ('2020-02-12', 'Depositing 250 again today', 250), 
  ]
  
  for tdate, desc, amount in deposits:
    deposit = {
      "medium": "balance",
      "transaction_date": tdate,
      "status": "pending",
      "description": desc,
      "amount": amount
    }
    resp = nessie.post('/accounts/' + account_id + '/deposits', deposit)

  withdrawals = [
    ('2020-10-25', 'Birthday Gift', 50), 
    ('2020-09-15', 'Food', 50), 
    ('2020-07-31', 'Food', 20), 
    ('2020-06-26', 'Video Game', 40), 
    ('2020-06-16', 'Candy', 10), 
    ('2020-05-01', 'Food', 50), 
  ]
  
  for tdate, desc, amount in withdrawals:
    deposit = {
      "medium": "balance",
      "transaction_date": tdate,
      "status": "pending",
      "description": desc,
      "amount": amount
    }
    resp = nessie.post('/accounts/' + account_id + '/withdrawals', deposit)

def add_rent(account_id):

  nessie = Nessie()

  for month in range(5, 11):  
    withdrawal = {
      'medium': 'balance',
      'transaction_date': '{:04}-{:02}-01'.format(2020, month),
      'status': 'pending',
      'description': 'Rent Payment',
      'amount': 500
    }
    resp = nessie.post('/accounts/' + account_id + '/withdrawals', withdrawal)

if __name__ == '__main__':
  main()