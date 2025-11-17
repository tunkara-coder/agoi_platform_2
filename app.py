from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'
app.config['UPLOAD_FOLDER'] = 'data/uploads'

# Initialize database
def init_db():
    conn = sqlite3.connect('agesi_platform.db')
    conn.row_factory = sqlite3.Row
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            region TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS country_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER,
            year INTEGER,
            policy_score REAL,
            sectoral_score REAL,
            finance_score REAL,
            human_capital_score REAL,
            overall_score REAL,
            tier TEXT
        )
    ''')
    
    # Add sample countries
    sample_countries = [
        ('Nigeria', 'NGA', 'West Africa'),
        ('Kenya', 'KEN', 'East Africa'), 
        ('South Africa', 'ZAF', 'Southern Africa'),
        ('Ethiopia', 'ETH', 'East Africa'),
        ('Ghana', 'GHA', 'West Africa')
    ]
    
    for country in sample_countries:
        conn.execute('INSERT OR IGNORE INTO countries (name, code, region) VALUES (?, ?, ?)', country)
    
    # Add sample scores
    sample_scores = [
        (1, 2023, 0.75, 0.65, 0.60, 0.55, 0.64, 'Emerging'),
        (2, 2023, 0.85, 0.75, 0.70, 0.65, 0.74, 'Frontrunner'),
        (3, 2023, 0.90, 0.80, 0.85, 0.75, 0.83, 'Frontrunner'),
        (4, 2023, 0.60, 0.70, 0.50, 0.45, 0.56, 'High Potential'),
        (5, 2023, 0.70, 0.60, 0.55, 0.50, 0.59, 'Emerging')
    ]
    
    for score in sample_scores:
        conn.execute('''
            INSERT OR REPLACE INTO country_scores 
            (country_id, year, policy_score, sectoral_score, finance_score, human_capital_score, overall_score, tier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', score)
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()
print("Database initialized successfully!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('agesi_platform.db')
    conn.row_factory = sqlite3.Row
    
    scores = conn.execute('''
        SELECT cs.*, c.name as country_name, c.code as country_code 
        FROM country_scores cs 
        JOIN countries c ON cs.country_id = c.id 
        WHERE cs.year = 2023
        ORDER BY cs.overall_score DESC
    ''').fetchall()
    
    # Calculate averages
    averages = conn.execute('''
        SELECT 
            AVG(policy_score) as policy,
            AVG(sectoral_score) as sectoral, 
            AVG(finance_score) as finance,
            AVG(human_capital_score) as human_capital
        FROM country_scores WHERE year = 2023
    ''').fetchone()
    
    conn.close()
    
    pillar_avgs = {
        'policy': averages['policy'] or 0,
        'sectoral': averages['sectoral'] or 0,
        'finance': averages['finance'] or 0, 
        'human_capital': averages['human_capital'] or 0,
        'overall_score': ((averages['policy'] or 0) + (averages['sectoral'] or 0) + 
                         (averages['finance'] or 0) + (averages['human_capital'] or 0)) / 4
    }
    
    return render_template('dashboard.html', scores=scores, pillar_avgs=pillar_avgs, current_year=2023)

@app.route('/country/<country_code>')
def country_profile(country_code):
    conn = sqlite3.connect('agesi_platform.db')
    conn.row_factory = sqlite3.Row
    
    country = conn.execute('SELECT * FROM countries WHERE code = ?', (country_code,)).fetchone()
    
    if not country:
        conn.close()
        flash('Country not found', 'error')
        return redirect('/dashboard')
    
    scores = conn.execute('SELECT * FROM country_scores WHERE country_id = ? ORDER BY year DESC', (country['id'],)).fetchall()
    conn.close()
    
    return render_template('country_profile.html', country=country, scores=scores)

@app.route('/data-upload')
def data_upload():
    return render_template('data_upload.html')

@app.route('/calculations')
def calculations():
    return render_template('calculations.html')

# Pillar detail routes
@app.route('/pillar/policy')
def policy_pillar():
    return render_template('policy.html')

@app.route('/pillar/sectoral')
def sectoral_pillar():
    return render_template('sectoral.html')

@app.route('/pillar/finance')
def finance_pillar():
    return render_template('finance.html')

@app.route('/pillar/human-capital')
def human_capital_pillar():
    return render_template('human_capital.html')

@app.route('/api/country-scores')
def api_country_scores():
    year = request.args.get('year', 2023, type=int)
    
    conn = sqlite3.connect('agesi_platform.db')
    conn.row_factory = sqlite3.Row
    
    scores = conn.execute('''
        SELECT cs.*, c.name as country_name, c.code as country_code 
        FROM country_scores cs 
        JOIN countries c ON cs.country_id = c.id 
        WHERE cs.year = ?
        ORDER BY cs.overall_score DESC
    ''', (year,)).fetchall()
    
    conn.close()
    
    data = []
    for score in scores:
        data.append({
            'country': score['country_name'],
            'code': score['country_code'],
            'policy_score': score['policy_score'] or 0,
            'sectoral_score': score['sectoral_score'] or 0,
            'finance_score': score['finance_score'] or 0,
            'human_capital_score': score['human_capital_score'] or 0,
            'overall_score': score['overall_score'] or 0,
            'tier': score['tier'] or 'Not Rated'
        })
    
    return jsonify(data)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print("Starting AGOI Platform...")
    print("Access at: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)