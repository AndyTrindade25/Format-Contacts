from flask import Flask, render_template, request, send_file
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['csv_file']
        if uploaded_file.filename != '':
            ddd = '62'
            coluna = ['Name', 'Phone 1 - Value']
            data = []

            try:
                csv_data = uploaded_file.read().decode('utf-8').splitlines()
                reader_csv = csv.DictReader(csv_data)

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

                output_csv = 'contatoFormatado.csv'
                output_stream = io.StringIO()
                csv_writer = csv.writer(output_stream)
                csv_writer.writerow(coluna)
                csv_writer.writerows(data)

                response = send_file(output_stream, as_attachment=True, attachment_filename=output_csv)
                response.headers["Content-Disposition"] = f"attachment; filename={output_csv}"
                return response

            except Exception as e:
                return f'Ocorreu um erro ao processar o arquivo CSV: {str(e)}'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
