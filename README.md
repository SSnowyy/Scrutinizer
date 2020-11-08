The Scrutinizer 2020!

Description:

Create an API that could be used by financial institutions, to monitor client transactions, and use machine learning to identify patterns that would suggest a possible anomalous situation in which either the client or financial institution should receive a warning.
For example, if a client made a sufficiently similar transaction close to the same time each month, say to pay the rent, and the client is currently (sufficiently) late, then the API would indicate that a warning should be presented to the user that they may be missing a payment.
For our hackathon demo, we used the Nessie API provided by Capital One to simulate bank transactions, and create a website to simulate displaying these transactions to a customer, providing a warning banner when a predicted payment is overdue.

Hackathon Technology Notes:

Use Capital One’s Nessie API to simulate a Bank

Use Google Cloud for creating the API, with DB

Use Google Cloud to create a simple website simulating a bank’s customer portal
.
This website will make API calls to both Nessie and The Scrutinizer to identify and display warnings to the customers.

The Scrutinizer will utilize Google Cloud’s machine learning service.

Use Postman to manually make API calls.

Store the project in Github.


Development Plan

Create a detailed description of the solution.

Identify technologies that will be used.

Create an architectural diagram, showing the servers involved and how they connect to each other.

Create a development plan (this), outlining the steps we need to take, including design, learning/experimenting, and implementation.

Create screen mock-ups of how our solution may appear to a user.

Learn how to call the Nessie API and what its capabilities are.

Experiment with making calls to Nessie using Postman.

Identify ways to POST transactions and GET all transactions for a customer.

Learn how to start a website in google cloud from the Hackathon available resources.

Identify and select a backing language.

Learn how to use a simple database backing.

Identify ways to handle POST transactions in a similar manner as Nessie.

Identify ways to GET suggestions for a specified customer.

Create simple website to simulate 

Call Nessie to GET all transactions for a fixed user.

Call The Scrutinizer 2020 to get suggestions.

Display transactions in a table.
