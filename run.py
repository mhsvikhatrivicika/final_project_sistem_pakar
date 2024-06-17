
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import hashlib
import mysql.connector
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='sistem_pakar'
)

# Function to check login
def check_login(username, password):
    cursor = db.cursor(dictionary=True)
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    query = "SELECT * FROM tbl_m_users WHERE username_tmu = %s AND password_tmu = %s"
    cursor.execute(query, (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    return user

# Routes for login and dashboard
@app.route('/pindah_login')
def pindah_login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = check_login(username, password)
        if user:
            session['username'] = username  # Simpan informasi pengguna ke dalam sesi
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard', username=username))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('admin/dashboard.html', username=username)

# Function to register user
def register_user(username, password):
    cursor = db.cursor()
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    try:
        query = "INSERT INTO tbl_m_users (username_tmu, password_tmu) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        db.commit()
        flash('Registration successful! Please login.', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
    finally:
        cursor.close()


# Rute untuk menampilkan halaman register dengan daftar pengguna
@app.route('/pindah_register')
def pindah_register():
    users = get_all_users()  # Dapatkan daftar semua pengguna
    return render_template('admin/register.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            register_user(username, password)
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match.', 'danger')
    
    return render_template('admin/register.html')

# Tambahkan fungsi untuk mendapatkan daftar semua pengguna
def get_all_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_tmu, username_tmu FROM tbl_m_users")
    users = cursor.fetchall()
    cursor.close()
    return users

# Tambahkan rute dan fungsi untuk reset kata sandi
@app.route('/reset_password/<int:user_id>', methods=['POST'])
def reset_password(user_id):
    cursor = db.cursor()
    default_password = '123123'
    hashed_password = hashlib.md5(default_password.encode()).hexdigest()
    try:
        cursor.execute("UPDATE tbl_m_users SET password_tmu = %s WHERE id_tmu = %s", (hashed_password, user_id))
        db.commit()
        flash('Password has been reset to 123123.', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('pindah_register'))

# Tambahkan rute dan fungsi untuk menghapus akun
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM tbl_m_users WHERE id_tmu = %s", (user_id,))
        db.commit()
        flash('User has been deleted.', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('pindah_register'))

# CRUD operations for linguistic data
@app.route('/pindah_linguistics')
def pindah_linguistics():
    linguistic = get_linguistic()
    return render_template('admin/lingustics.html', linguistic=linguistic)

def get_linguistic():
    cursor = db.cursor()
    cursor.execute("SELECT l.id_tml, v.name_tmv, l.label_tml, l.a_tml, l.b_tml, l.c_tml, l.d_tml FROM tbl_m_linguistic l INNER JOIN tbl_m_variabel v ON l.id_tmv = v.id_tmv")
    linguistic = cursor.fetchall()
    cursor.close()
    return linguistic


def add_linguistic(name_tmv, label_tml, a_tml, b_tml, c_tml, d_tml):
    cursor = db.cursor()
    query = """
    INSERT INTO tbl_m_linguistic (id_tmv, label_tml, a_tml, b_tml, c_tml, d_tml)
    SELECT id_tmv, %s, %s, %s, %s, %s FROM tbl_m_variabel WHERE name_tmv = %s
    """
    cursor.execute(query, (label_tml, a_tml, b_tml, c_tml, d_tml, name_tmv))
    db.commit()
    cursor.close()


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name_tmv = request.form['name_tmv']
        label_tml = request.form['label_tml']
        a_tml = request.form['a_tml']
        b_tml = request.form['b_tml']
        c_tml = request.form['c_tml']
        d_tml = request.form['d_tml']
        add_linguistic(name_tmv, label_tml, a_tml, b_tml, c_tml, d_tml)
        flash('Linguistic data added successfully', 'success')
        return redirect('/pindah_linguistics')

@app.route('/edit/<int:id_tml>', methods=['POST', 'GET'])
def edit(id_tml):
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT l.id_tml, v.name_tmv, l.label_tml, l.a_tml, l.b_tml, l.c_tml, l.d_tml FROM tbl_m_linguistic l INNER JOIN tbl_m_variabel v ON l.id_tmv = v.id_tmv WHERE l.id_tml = %s", (id_tml,))
        linguistic = cursor.fetchone()
        return render_template('admin/edit_lingustics.html', linguistic=linguistic)
    if request.method == 'POST':
        label_tml = request.form['label_tml']
        a_tml = request.form['a_tml']
        b_tml = request.form['b_tml']
        c_tml = request.form['c_tml']
        d_tml = request.form['d_tml']
        cursor.execute("UPDATE tbl_m_linguistic SET label_tml = %s, a_tml = %s, b_tml = %s, c_tml = %s, d_tml = %s WHERE id_tml = %s",
                       (label_tml, a_tml, b_tml, c_tml, d_tml, id_tml))
        db.commit()
        cursor.close()
        flash('Linguistic data updated successfully', 'success')
        return redirect('/pindah_linguistics')


@app.route('/delete/<int:id_tml>', methods=['POST'])
def delete(id_tml):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tbl_m_linguistic WHERE id_tml = %s", (id_tml,))
    db.commit()
    cursor.close()
    flash('Linguistic data deleted successfully', 'success')
    return redirect('/pindah_linguistics')

# CRUD operations for fuzzy rules
@app.route('/pindah_rule')
def pindah_rule():
    variables_input = get_input_variables()
    variables_output = get_output_variables()
    rules = get_rules()
    return render_template('admin/rule.html', variables_input=variables_input, variables_output=variables_output, rules=rules)

def get_rules():
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            r.id_ttfr,
            v.name_tmv AS variable_name,
            l.label_tml AS label_name,
            r.rule_ttfr AS rule,
            r.output_ttfr AS output_name
        FROM
            tbl_t_fuzzy_rules r
        INNER JOIN
            tbl_m_variabel v ON r.id_tmv = v.id_tmv
        INNER JOIN
            tbl_m_linguistic l ON r.id_tml = l.id_tml
    """)
    rules = cursor.fetchall()
    cursor.close()
    return rules

def get_input_variables():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_m_variabel WHERE type_tmv = 'input'")
    variables = cursor.fetchall()
    cursor.close()
    return variables

def get_output_variables():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_m_variabel WHERE type_tmv = 'output'")
    variables = cursor.fetchall()
    cursor.close()
    return variables

def get_labels(id_tmv):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_m_linguistic WHERE id_tmv = %s", (id_tmv,))
    labels = cursor.fetchall()
    cursor.close()
    return labels

@app.route('/add_rule', methods=['POST'])
def add_rule():
    if request.method == 'POST':
        id_tmv = request.form['name_tmv']
        id_tml = request.form['label_tml']
        rule_ttfr = request.form['rule_ttfr']
        output_ttfr = request.form['output_ttfr']
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO tbl_t_fuzzy_rules (id_tmv, id_tml, rule_ttfr, output_ttfr) VALUES (%s, %s, %s, %s)", (id_tmv, id_tml, rule_ttfr, output_ttfr))
        db.commit()
        cursor.close()
        flash('Rule added successfully', 'success')
        return redirect('/pindah_rule')

@app.route('/edit_rule/<int:id_ttfr>', methods=['GET', 'POST'])
def edit_rule(id_ttfr):
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM tbl_t_fuzzy_rules WHERE id_ttfr = %s", (id_ttfr,))
        rule = cursor.fetchone()
        cursor.close()
        variables_input = get_input_variables()
        variables_output = get_output_variables()
        labels = get_labels(rule[1]) if rule else []
        return render_template('admin/edit_rule.html', rule=rule, variables_input=variables_input, variables_output=variables_output, labels=labels)
    elif request.method == 'POST':
        id_tmv = request.form['id_tmv']
        id_tml = request.form['id_tml']
        rule_ttfr = request.form['rule_ttfr']
        output_ttfr = request.form['output_ttfr']
        
        cursor.execute("UPDATE tbl_t_fuzzy_rules SET id_tmv = %s, id_tml = %s, rule_ttfr = %s, output_ttfr = %s WHERE id_ttfr = %s", (id_tmv, id_tml, rule_ttfr, output_ttfr, id_ttfr))
        db.commit()
        cursor.close()
        flash('Rule updated successfully', 'success')        # Handling the response and redirecting appropriately
        return redirect('/pindah_rule')

@app.route('/delete_rule/<int:id_ttfr>', methods=['POST'])
def delete_rule(id_ttfr):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tbl_t_fuzzy_rules WHERE id_ttfr = %s", (id_ttfr,))
    db.commit()
    cursor.close()
    flash('Rule deleted successfully', 'success')
    return redirect('/pindah_rule')

# AJAX route to load labels based on selected variable
@app.route('/load_labels')
def load_labels():
    id_tmv = request.args.get('id_tmv')
    labels = get_labels(id_tmv)
    return jsonify({'labels': labels})

# CRUD operations for variables
@app.route('/pindah_variabel')
def pindah_variabel():
    variabels = get_variabels()
    return render_template('admin/var.html', variabels=variabels)

def get_variabels():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_m_variabel")
    return cursor.fetchall()

def get_variabel(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_m_variabel WHERE id_tmv = %s", (id,))
    return cursor.fetchone()

def get_variabels_tanpa_output():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_m_variabel WHERE type_tmv='input'")
    return cursor.fetchall()

def add_variabel(name, type, question):
    cursor = db.cursor()
    cursor.execute("INSERT INTO tbl_m_variabel (name_tmv, type_tmv, question_tmv) VALUES (%s, %s, %s)", (name, type, question))
    db.commit()
    cursor.close()

def update_variabel(id, name, type, question):
    cursor = db.cursor()
    cursor.execute("UPDATE tbl_m_variabel SET name_tmv = %s, type_tmv = %s, question_tmv = %s WHERE id_tmv = %s", (name, type, question, id))
    db.commit()
    cursor.close()

def delete_variabel(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tbl_m_variabel WHERE id_tmv = %s", (id,))
    db.commit()
    cursor.close()
    

@app.route('/add_var', methods=['POST'])
def add_var():
    name = request.form['name']
    type = request.form['type']
    question = request.form['question']
    add_variabel(name, type, question)
    flash('Variabel added successfully!', 'success')
    return redirect('/pindah_variabel')

@app.route('/edit_var/<int:id>')
def edit_var(id):
    variabel = get_variabel(id)
    return render_template('admin/edit_var.html', variabel=variabel)

@app.route('/update_var/<int:id>', methods=['POST'])
def update_var(id):
    name = request.form['name']
    type = request.form['type']
    question = request.form['question']
    update_variabel(id, name, type, question)
    flash('Variabel updated successfully!', 'success')
    return redirect('/pindah_variabel')

@app.route('/delete_var/<int:id>')
def delete_var(id):
    delete_variabel(id)
    flash('Variabel deleted successfully!', 'success')
    return redirect('/pindah_variabel')

# Fuzzy logic and simulation

# Function to create custom antecedent with linguistic labels
# Route to render index.html page
@app.route('/')
def index():
    variabels = get_variabels_tanpa_output()
    return render_template('index.html', vari=variabels)

@app.route('/pindah_admin')
def pindah_admin():
    return render_template('admin/dashboard.html')

# Define the fuzzy variables and rules
    
# Function to create custom antecedent from database
def create_custom_antecedent(name, range_values, linguistic_labels):
    antecedent = ctrl.Antecedent(np.arange(*range_values), name)
    
    for label, trapmf_values in linguistic_labels.items():
        antecedent[label] = fuzz.trapmf(antecedent.universe, trapmf_values)
    
    return antecedent

# Function to create consequent from database
def create_consequent(name, range_values, linguistic_labels):
    consequent = ctrl.Consequent(np.arange(*range_values), name)
    
    for idx, label in enumerate(linguistic_labels):
        consequent[label] = fuzz.trapmf(consequent.universe, [idx + 1, idx + 1, idx + 1, idx + 1])  # Default trapmf values
    
    return consequent

# Function to fetch input variable definitions from database
def fetch_input_var_definitions():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name_tmv FROM tbl_m_variabel WHERE type_tmv = 'input'")
    return [{'var_name': row['name_tmv']} for row in cursor.fetchall()]

# Function to create custom antecedent from database
def create_custom_antecedent_from_db(var_name):
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM tbl_m_linguistic WHERE id_tmv = (SELECT id_tmv FROM tbl_m_variabel WHERE name_tmv = '{var_name}')")
    linguistic_labels = {}
    for row in cursor.fetchall():
        linguistic_labels[row['label_tml']] = [row['a_tml'], row['b_tml'], row['c_tml'], row['d_tml']]
    return create_custom_antecedent(var_name, range_values, linguistic_labels)


def create_consequent(name, range_values, linguistic_labels):
    consequent = ctrl.Consequent(np.arange(*range_values), name)
    consequent.automf(3, names=linguistic_labels)
    return consequent

# Define range values for fuzzy variables
range_values = (1, 11, 1)
range_values_output = (1, 7, 1)

# Initialize input variable definitions using database values
input_var_definitions = fetch_input_var_definitions()

# Initialize input variables using database values
input_vars = {
    item['var_name']: create_custom_antecedent_from_db(item['var_name'])
    for item in input_var_definitions
}

# Definisi trapmf untuk output variables
output_linguistic_labels = {
    'otoriter': [1, 2, 2, 3],
    'tidak_terlibat': [2, 3, 3, 4],
    'demokratis': [3, 4, 4, 5],
    'permisif': [4, 5, 5, 6]
}

# Inisialisasi variabel output dengan trapmf
output_var = create_consequent('pola_asuh', range_values_output, output_linguistic_labels)


# Mendefinisikan aturan fuzzy dari data di database
cursor = db.cursor()
sql_query = "SELECT * FROM vw_fuzzy_rules"
cursor.execute(sql_query)
rules_data = []
for row in cursor:
    rule_data = {
        'rule': row[1],
        'variable': row[2],
        'linguistic': row[3],
        'output': row[4]
    }
    rules_data.append(rule_data)
cursor.close()

def define_rules_from_data(rules_data, input_vars, output_var):
    rules_dict = {}
    rules = []
    for item in rules_data:
        rule_id = item['rule']
        if rule_id not in rules_dict:
            rules_dict[rule_id] = []
        rules_dict[rule_id].append(item)

    for rule_id, conditions in rules_dict.items():
        antecedent = None
        for condition in conditions:
            var_name = condition['variable']
            linguistic_value = condition['linguistic']
            if antecedent is None:
                antecedent = input_vars[var_name][linguistic_value]
            else:
                antecedent &= input_vars[var_name][linguistic_value]
        output = conditions[0]['output']
        rule = ctrl.Rule(antecedent, output_var[output])
        rules.append(rule)
    return rules

# Definisikan aturan fuzzy dari data
fuzzy_rules = define_rules_from_data(rules_data, input_vars, output_var)

# Fungsi untuk menjalankan simulasi dan mendapatkan nilai keanggotaan output
def simulate(inputs, rules, input_values):
    # Buat sistem kontrol dan simulasi
    control_system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(control_system)
    
    # Masukkan nilai-nilai input
    for var, value in input_values.items():
        simulation.input[var] = value
    
    try:
        # Hitung simulasi
        simulation.compute()
        output_value = simulation.output['pola_asuh']
        
        # Dapatkan nilai keanggotaan untuk setiap label linguistik output
        membership_values = {label: fuzz.interp_membership(output_var.universe, output_var[label].mf, output_value)
                             for label in output_linguistic_labels}
        
        # Dapatkan label dengan nilai keanggotaan terbesar
        max_membership_label = max(output_linguistic_labels, key=lambda label: membership_values[label])
        
        # Dapatkan nilai keanggotaan terbesar
        max_membership_value = membership_values[max_membership_label]
        
        # Tampilkan hasil output
        print(f"Pola Asuh: {max_membership_label.capitalize()}")
        print(f"Nilai Keanggotaan Terbesar: {max_membership_value:.4f}")
        
        return output_value, membership_values, max_membership_label.capitalize()
      
            
    except (AssertionError, ValueError):
        return None, None, "-"


# Rute untuk menerima input dan memberikan output
@app.route('/fuzzy', methods=['POST'])
def fuzzy_logic():
    input_values = {key: int(value) for key, value in request.json.items()}
    
    output_value, membership_values, pola_asuh = simulate(input_vars, fuzzy_rules, input_values)
    
    # Simpan hasil ke session
    session['output_value'] = output_value
    session['pola_asuh'] = pola_asuh
    session['membership_values'] = membership_values
    
    response = {
        "output_value": output_value,
        "membership_values": membership_values,
        "pola_asuh": pola_asuh
    }
    
    return jsonify(response)


@app.route('/hasil_fuzzy')
def hasil_fuzzy():
    if 'output_value' in session and 'pola_asuh' in session and 'membership_values' in session:
        output_value = session['output_value']
        pola_asuh = session['pola_asuh']
        membership_values = session['membership_values']
    else:
        output_value = None
        pola_asuh = None
        membership_values = None
    
    return render_template('hasil_fuzzy.html', output_value=output_value, pola_asuh=pola_asuh, membership_values=membership_values)


@app.route('/logout')
def logout():
    session.pop('username', None)  # Hapus informasi sesi yang relevan
    return redirect(url_for('pindah_login'))  # Redirect ke halaman login atau halaman lain yang sesuai


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
