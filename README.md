# Secure User Authentication System

First Phase:
This project implements a secure user authentication system using Flask, PostgreSQL, bcrypt, and regular expressions. The system ensures that user passwords are stored securely and follows strong complexity requirements. 

The aim is to create a couple of endpoints centered towards user authentication requirements. 

##### POST /createuser  
This creates a new user and returns a uuid
  
###### Request & Response headers  
Content-Type: application/json  
  
###### Body  
```  
{  
     "username": "xusername",
    "password": "Xxxxxxxx@1"
}  
```

###### Success Response  
* Status code: 201
* Content: `{ "uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" }`

##### POST /login  
Checks if the user is already registered and then logins him in 
  
###### Request & Response headers  
Content-Type: application/json  
  
###### Body  
```  
{  
     "username": "xusername",
    "password": "Xxxxxxxx@1"
}  
```

###### Success Response  
* Status code: 200
* Content: ` {"message": "Login successful"} 

The code handles multiple exceptions and error handling, it makes sure the user has a strong password and tries to make a seamless experience for a user to create a new account as well as login without any hassel. 
