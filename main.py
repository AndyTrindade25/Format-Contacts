from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import csv
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    headers = []
    return render_template('index.html', headers=headers)

@app.route('/process_csv', methods=['POST'])
def process_csv():
    headers = []  # Inicialize a variável headers como uma lista vazia
    uploaded_file = request.files['csv_file']
    ddd = request.form.get('ddd')

    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'contato.csv')
        uploaded_file.save(file_path)

        # Get the CSV headers
        with open(file_path, 'r') as file_csv:
            reader_csv = csv.DictReader(file_csv)
            headers = reader_csv.fieldnames  # Atualize a variável headers com os cabeçalhos do CSV

    name_column = request.form.get('name_column')
    phone_column = request.form.get('phone_column')

    if name_column and phone_column:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'contato.csv')

        coluna = [name_column, phone_column]
        data = []

        try:
            with open(file_path, 'r') as file_csv:
                reader_csv = csv.DictReader(file_csv)

                for row in reader_csv:
                    name = row[name_column]
                    phone = row[phone_column]

                    phone = phone.replace(' ', '').replace('-', '').replace('+', '').replace('(', '').replace(')', '').replace('+', '').replace(':', '').replace('*', '')

                    if len(phone) <= 13:
                        if phone.startswith('0'):
                            phone = '55' + phone[1:]
                        if len(phone) == 11 or len(phone) == 10:
                            phone = '55' + phone
                        if len(phone) < 10:
                            phone = '55' + ddd + phone
                        if len(phone) > 9:
                            data.append([name, phone])

            formatted_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'contatosFormatados.csv')

            with open(formatted_csv_path, 'w', newline='') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(coluna)
                csv_writer.writerows(data)

            return redirect(url_for('download', filename='contatosFormatados.csv'))

        except Exception as e:
            print(f'Ocorreu um erro ao processar o arquivo CSV: {str(e)}')
            return f'Ocorreu um erro ao processar o arquivo CSV: {str(e)}'

    return 'Selecione as colunas corretas para o nome e o telefone.'

@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8099)
