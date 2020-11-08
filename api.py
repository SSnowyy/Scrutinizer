from flask import Flask, jsonify, request
from nessie import Nessie
from scrutinize import Scrutinize
import requests
from datetime import datetime, date
import statistics
import seed

app = Flask(__name__)
nessie = Nessie()
scrutinize_client = Scrutinize()

# http://127.0.0.1:5000/history?accountid=5fa7529bf1bac107157e1d8d
# http://127.0.0.1:5000/history?accountid=5fa7549ff1bac107157e1d97

@app.route('/history')
def history():

  s = get_head()
  
  s += show_buttons()
  
  #s += show_info()
  
  #account_id = request.args.get('accountid')
  account_id = get_account_id()
  
  #s += 'You selected account id ' + account_id + '<br/>'
  
  account = nessie.get('/accounts/' + account_id)  

  if not account:
    s += 'Account not found.<br/>'
  else:
  
    warnings = scrutinize_client.get('/scrutinize/' + account_id)
	
    related = {}
    if len(warnings) > 0:
      s += show_alerts(warnings)
      for warning in warnings:
        #s += str(warning['related'])
        for id in warning['related']:
          related[id] = True

    deposits = nessie.get('/accounts/' + account_id + '/deposits')
    withdrawals = nessie.get('/accounts/' + account_id + '/withdrawals')
  
    transactions = sorted(deposits + withdrawals, key=lambda t: t['transaction_date'], reverse=True)

    s += show_transaction_table(transactions, related) 
  
  s += get_tail()
	
  return s

def show_transaction_table(transactions, highlight):

  s = ''
  s += '<table id="transactions">'
  s += '  <tr>'
  s += '    <th>Transaction Date</th>'
  s += '    <th>Type</th>'
  s += '    <th>Description</th>'
  s += '    <th>Amount</th>'
  s += '  </tr>'
  
  for trans in transactions:
    if trans['_id'] in highlight:
      s += '  <tr style="background-color: #EEAA99">'
      #s += '  <tr class="related">'
    else:
      s += '  <tr>'
    s += '    <td>{}</td>'.format(trans['transaction_date'])
    s += '    <td>{}</td>'.format(trans['type'])
    s += '    <td>{}</td>'.format(trans['description'])
    s += '    <td>${:0,.2f}</td>'.format(trans['amount'])
    s += '  </tr>'

  s += '</table>'
  
  return s

def show_alerts(warnings):

  s = ''
  for warning in warnings:
    s += '<div class="alert">'
    s += '<span class="closebtn" onclick="this.parentElement.style.display=\'none\';">&times;</span> '
    s += '<strong>Warning!</strong> You may be missing a payment for "{}".'.format(warning['description'])
    s += '</div>' 
  
  return s
  
def show_info():

  customers = nessie.get('/customers')

  s = ''
  for customer in customers:
    s += 'Customer: ' + customer['_id'] + '<br/>'
    
    accounts = nessie.get('/customers/{}/accounts'.format(customer['_id']))
    for account in accounts:
      s += '&nbsp;&nbsp;Account: ' + account['_id'] + '<br/>'
 
  return s

def show_buttons():
  s = ''
  
  s += '<div id="stage" style="background-color:cc0;" hidden>STAGE</div>'
  s += '<div align="center">'
  s += '<input type="button" class="button" id="reset" value="Reset Data" width="50" />'
  s += '&nbsp;&nbsp;&nbsp;'
  s += '<input type="button" class="button" id="addrent" value="Add Rent Payments" />'
  s += '&nbsp;&nbsp;&nbsp;'
  s += '<input type="reload" class="button" value="Reload Page" onclick="history.go(0);" />'
  s += '</div><br/><br/>'
  
  return s
      
@app.route('/scrutinize/<id>')
def scrutinize(id):

  withdrawals = nessie.get('/accounts/' + id + '/withdrawals')

  # analyze for missing withdrawal...
  descriptions_to_warn = analyze(withdrawals)

  warnings = []  
  for desc in descriptions_to_warn:
    related = []
    for wd in withdrawals:
      if wd['description'] == desc:
        related.append(wd['_id'])
  
    warnings.append(
      {
        'kind':'PossibleLate',
        'severity':'High',
        'confidence':'90',
        'description':desc,
        'related': related
      })
  
  return jsonify(warnings)
  
@app.route('/reset')
def reset():
  seed.reset_data()
  return jsonify({'IsSuccess':True})

@app.route('/add-rent')
def add_rent():
  seed.add_rent(get_account_id())
  return jsonify({'IsSuccess':True})
  
def analyze(withdrawals):

  x = {}

  for wd in withdrawals:
    dt = datetime.strptime(wd['transaction_date'], '%Y-%m-%d')
    if wd['description'] in x:
      x[wd['description']].append(dt.toordinal())
    else:
      x[wd['description']] = [dt.toordinal()]

  warn = []
  for key in x:
    x[key] = [x[key][i]-x[key][i-1] for i in range(1, len(x[key]))]

    if len(x[key]) > 2:
      mean = statistics.mean(x[key])
      if all([abs(x[key][i] - mean) < 5 for i in range(len(x[key]))]):
        x[key][-1] + int(mean)
        if date.today().toordinal() > x[key][-1] + int(mean) + 5:
          warn.append(key)

  return warn

def get_account_id():
  customers = nessie.get('/customers')
  accounts = nessie.get('/customers/{}/accounts'.format(customers[0]['_id']))
  return accounts[0]['_id']

def get_head():
  return """
<html>
<head>
<script type = "text/javascript" 
  src = "https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js">
</script>

<script type = "text/javascript" language = "javascript">
  $(document).ready(function() {
    $("#reset").click(function(event){
      $('#stage').load('/reset');
    });
    $("#addrent").click(function(event){
      $('#stage').load('/add-rent');
    });
  });
</script>

<style>
#transactions {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#transactions td, #transactions th {
  border: 1px solid #ddd;
  padding: 8px;
}

#transactions tr:nth-child(even){background-color: #f2f2f2;}

#transactions tr:hover {background-color: #ddd;}

#transactions th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}
</style>

<style>
.alert {
  padding: 20px;
  background-color: #f44336;
  color: white;
}

.closebtn {
  margin-left: 15px;
  color: white;
  font-weight: bold;
  float: right;
  font-size: 22px;
  line-height: 20px;
  cursor: pointer;
  transition: 0.3s;
}

.closebtn:hover {
  color: black;
}

.related {
  background-color: #EEAA99
}

.button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  width: 200px;
}
</style>

</head>
<body>"""

def get_tail():
  return '</body></html>'


if __name__ == '__main__':
  app.run(debug=True)