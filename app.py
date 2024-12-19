from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid
import random

app = Flask(__name__)

DATABASE = 'secret_santa.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                participants TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                event_id TEXT,
                giver TEXT,
                receiver TEXT,
                PRIMARY KEY (event_id, giver)
            )
        ''')

@app.route('/')
def home():
    return render_template('create_event.html')

@app.route('/create', methods=['POST'])
def create_event():
    participants = request.form['participants'].strip().split('\n')
    participants = [p.strip() for p in participants if p.strip()]
    if len(participants) < 2:
        return "You need at least two participants!", 400

    event_id = str(uuid.uuid4())
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (id, participants) VALUES (?, ?)',
                       (event_id, '\n'.join(participants)))

    event_link = f"{request.url_root}event/{event_id}"
    return render_template('event_ready.html', link=event_link)

@app.route('/event/<event_id>', methods=['GET', 'POST'])
def assign(event_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT participants FROM events WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        if not row:
            return "Event not found!", 404

        participants = row[0].split('\n')

        if request.method == 'POST':
            giver = request.form['name'].strip()
            cursor.execute('SELECT receiver FROM assignments WHERE event_id = ? AND giver = ?',
                           (event_id, giver))
            assignment = cursor.fetchone()

            if assignment:
                return render_template('assigned.html', receiver=assignment[0])
            else:
                available = set(participants) - set(
                    row[0] for row in cursor.execute('SELECT receiver FROM assignments WHERE event_id = ?', (event_id,))
                )
                if giver not in participants:
                    return "Invalid participant!", 400

                if not available:
                    return "All assignments complete!", 400

                receiver = random.choice(list(available - {giver}))
                cursor.execute('INSERT INTO assignments (event_id, giver, receiver) VALUES (?, ?, ?)',
                               (event_id, giver, receiver))
                conn.commit()
                return render_template('assigned.html', receiver=receiver)

        return render_template('assign.html', event_id=event_id, participants=participants)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
