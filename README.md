# Bank-TransactionsAPI
REST API using Flask

Steps to run the application:
1. Clone the repository: https://github.com/sathwika05/Bank-TransactionsAPI.git
2. Open the terminal navigate to the docker-compose.yml file in the project directory.
3. Run docker-compose up

Application Documentation: https://documenter.getpostman.com/view/19885819/UVkvJsNJ

BANK TRANSACTIONS REST APIs:

1. Registration API: Description: This API is used to create a new user. Endpoint: http://localhost:5000/register Request: { 
    "fullname":"Testcase1","username":"sathwika123","password":"xyz","phoneno":"937-815-4324"} Response: {"Status": 200,"message": "Successfully Signed Up"}
  
2. Add API: Description: This API is used to add the money to the existing user Endpoint: http://localhost:5000/add Request: {"username":"parshaboina123",
    "password":"sxp","amount":500} Response: {"Transaction_Id": "cbaeed41-cb32-403c-b2c7-42b26eb3a03e", "message": "Amount added successfully to account",
  "status": 200}

3. Transfer API: Description: This API is used to transfer the money from one account to the another account. Endpoint: http://localhost:5000/transfer Request: {
    "username":"parshaboina123","password":"sxp", "to":"sathwika123","amount":200 } Response: { "Transaction_Id": "27c5e899-376e-4f55-9052-7048e5b23b5d","message": "Amount Transferred successfully","status": 200}

4. Balance API: Description: This API is used to get the current balance in the account. Endpoint: http://localhost:5000/balance Request: {
    "username":"testcase1","password":"xyz"} Response:{"Debt": 0,"Own": 599,"Username": "testcase1"}

5. TakeLoan API: Description: This API is used to upadate the loan taken by the existing user. Endpoint: http://localhost:5000/takeloan Request: {
    "username":"parshaboina123","password":"sxp","amount":80} Response: {"Transaction_Id": "60169159-377b-429e-888b-a0b9d854c067","message": "Loan added to your account",
  "status": 200}
  
6. PayLoan API: Description: This API is used to pay the loan taken by the existing user Endpoint: http://localhost:5000/payloan Request: { "username":"parshaboina123",
    "password":"sxp","amount":80} Response: {"Transaction_Id": "70d19159-237a-655e-564c-e8471ba4c067","message":"You've successfully paid your loan","status":200}


