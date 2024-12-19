# Secret Santa App

This project is a web application for organizing a Secret Santa event. The app allows users to create an event, list participants, and distribute assignments anonymously. Participants can view their assignments via a unique event link. The app ensures that participants do not get themselves as their assignment and keeps all data secure.

---

## Features

1. **Create Event**:
    - Users can create a Secret Santa event by providing a list of participants.
    - A unique link is generated for the event.

2. **View Assignments**:
    - Participants can use the unique link to find out their gift recipient.
    - Each participant can only see their own assignment.

3. **Already Assigned Page**:
    - If a participant has already viewed their assignment, they are redirected to a page reminding them of their recipient.

4. **Security Enhancements**:
    - SQL injection protection with parameterized queries.
    - XSS protection by sanitizing user input.
    - CSRF protection using Flask-WTF.
    - Rate limiting to prevent abuse.

5. **Responsive Design**:
    - Festive, Christmas-themed UI built using Bootstrap.
    - Fully responsive and mobile-friendly.

---

## Project Structure

```
secret_santa/
├── app.py                # Main application logic
├── secret_santa.db       # SQLite database
├── templates/            # HTML templates
│   ├── create_event.html  # Event creation page
│   ├── assign.html        # Assignment page
│   ├── already_assigned.html # Already assigned page
├── static/               # Static files
│   ├── styles.css         # Custom styles
│   ├── bootstrap.min.css  # Bootstrap CSS
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Prerequisites

- Python 3.8+
- SQLite3

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/secret-santa-app.git
   cd secret-santa-app
   ```

2. **Install Dependencies**:
   Create a virtual environment and install dependencies from `requirements.txt`:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   Initialize the SQLite database:
   ```bash
   python
   >>> import sqlite3
   >>> conn = sqlite3.connect('secret_santa.db')
   >>> conn.execute('''CREATE TABLE events (
       id TEXT PRIMARY KEY,
       participants TEXT
   );''')
   >>> conn.execute('''CREATE TABLE assignments (
       event_id TEXT,
       giver TEXT,
       receiver TEXT,
       PRIMARY KEY (event_id, giver)
   );''')
   >>> conn.close()
   ```

4. **Run the Application**:
   Start the Flask development server:
   ```bash
   python app.py
   ```
   Access the app at [http://localhost:5000](http://localhost:5000).

---

## Security Features

- **SQL Injection Protection**:
    - All SQL queries use parameterized statements to prevent injection attacks.

- **XSS Protection**:
    - Input is sanitized and rendered with Jinja2's auto-escaping.

- **CSRF Protection**:
    - Flask-WTF ensures all forms include CSRF tokens.

- **Rate Limiting**:
    - Prevents abuse by limiting requests per user/IP address.

---

## Limitations

- Event links are unique but could be brute-forced; adding a secondary token or password can enhance security.
- SQLite is used for simplicity but may not scale well for larger use cases.

---

## Future Improvements

1. **Authentication**:
    - Implement user authentication for more control over event access.

2. **Event Expiration**:
    - Add an expiration date for events to reduce data retention.

3. **Advanced Security**:
    - Encrypt assignments using a server-side encryption key.

4. **Improved Scalability**:
    - Migrate to a more robust database like PostgreSQL.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Developed by [ChatGPT](https://chatgpt.com).

