import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from AI import AI
from add_csv_data import upload_csv_to_postgres

app = Flask(__name__)

app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/main")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['csv_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(csv_path)
            table_name = request.form['table_name']
            message = upload_csv_to_postgres(csv_path, table_name)
            flash(message)
            return redirect(url_for('landing'))
    return render_template('upload.html')

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    complete_command = f'''

            you are an expert Database enggineer and proficient in SQL queries. You know to solve  any type of problem.
            now you will get some instrutions from the user. you goal is to understand what user wants done and do the same, It will generally involve using your skills only.

            <user instructions start>  {prompt} <user instructions ends>

            Remember, you can use always use sql queries to know the schema if unsure, like you can always use desc table_name etc. do not ask silly questions if there is somehting that you can know
            youself by using a query go for it.
            Try to solve the problems yourself first, you have all the neccsary tools. Do not anounce you plan to user just execute it.
            Always Give the final response in a credible manner with proper details and all the data that was asked for.
            Always return text as the final response.

            respond according to the user instructions. Also be friendly and a good conversation.
            also do not return the quesries execute them . You are an engg not a consultant.
            
            Also at last always verify if this user needs were met or not correctly, verify own your own.


            '''
    
    response = AI(complete_command)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)