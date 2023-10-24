from flask import Flask, render_template, request, send_from_directory
import csv
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['csv_file']
        ddd = request.form.get('ddd')
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'contato.csv')
            uploaded_file.save(file_path)

            # Process the uploaded CSV file and save the formatted file
            coluna = ['Name', 'Phone 1 - Value']
            data = []

            try:
                with open(file_path, 'r') as file_csv:
                    reader_csv = csv.DictReader(file_csv)

                    for row in reader_csv:
                        name = row['Name']
                        phone = row['Phone 1 - Value']

                        phone = phone.replace(' ', '').replace('-', '').replace('+','').replace('(','').replace(')','').replace('+','').replace(':','').replace('*','')

                        if len(phone) <= 13:
                            if phone.startswith('0'):
                                phone = '55' + phone[1:]
                            if len(phone) <= 11:
                                phone = '55' + ddd + phone
                            if len(phone) > 9:
                                data.append([name, phone])

                formatted_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'contatoFormatado.csv')

                with open(formatted_csv_path, 'w', newline='') as output_file:
                    csv_writer = csv.writer(output_file)
                    csv_writer.writerow(coluna)
                    csv_writer.writerows(data)

                return render_template('download.html', filename='contatoFormatado.csv')

            except Exception as e:
                return f'Ocorreu um erro ao processar o arquivo CSV: {str(e)}'

    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
