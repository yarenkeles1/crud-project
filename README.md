# Flask User Management Platform with MSSQL & MongoDB Support

This project is a comprehensive web application for user management, developed using Flask. The application is designed to be compatible with both MSSQL and MongoDB databases, supporting user addition, deletion, update, and listing operations seamlessly.

One of the key features of the application is that the choice of database is left to the user. When launching the application, the user can select which database to use, and this choice is preserved using Flask sessions. This ensures that database switching is managed smoothly throughout the application. Additionally, flash messages provide immediate feedback to the user about performed actions, significantly enhancing the user experience.

The project offers high flexibility in terms of data access and management. When MongoDB is selected, data is stored in a collection, whereas with MSSQL, it is maintained in a relational table. This architecture makes it ideal for learning and testing different database management systems. All database operations are supported with error handling, ensuring that any connection issues or data errors are communicated to the user in a clear and understandable manner.

## Features

- Multi-database support: MSSQL and MongoDB.
- User management operations: add, update, delete, and list users.
- Flash messages for immediate feedback.
- Error handling for database operations.
- User-friendly HTML interface.

## HTML Templates

HTML templates are organized in the `templates/` folder, and each page is structured to simplify user interaction:

- `index.html` → Displays the list of users.
- `ekle.html` → Provides a form to add a new user.
- `sil.html` → Manages user deletion operations.
- `guncelle.html` → Provides a form to update user information.
- `veritabanisec.html` → Allows the user to select the database.

## Project Structure
```
Crud_Project/
├── flask_app.py           # Main Flask application
├── templates/             # HTML templates
│   ├── index.html
│   ├── ekle.html
│   ├── sil.html
│   ├── guncelle.html
│   └── veritabanisec.html
├── .env                   # Environment variables (SECRET_KEY, DB connections)
└── README.md              # Project documentation
```
