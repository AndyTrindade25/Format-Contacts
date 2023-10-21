import csv

name_csv = 'contato.csv'
output_csv = 'contatoFormatado.csv'

ddd = '17'

coluna = ['Name', 'Phone 1 - Value']

data = []

try:
    with open(name_csv, 'r') as file_csv:
        reader_csv = csv.DictReader(file_csv)

        for row in reader_csv:
            name = row['Name']
            phone = row['Phone 1 - Value']

            phone = phone.replace(' ', '').replace('-', '').replace('+','').replace('(','').replace(')','').replace('+','').replace(':','').replace('*','')

            if len(phone) <= 13:

                if phone.startswith('0'):
                    phone = '55' + phone[1:]
                
                if len(phone) < 10:
                    phone = '55' + ddd + phone
                if len(phone) > 9:
                    data.append([name, phone])
                

except FileNotFoundError:
    print(f'O arquivo {name_csv} não foi encontrado!')

except Exception as e:
    print(f'Ocorreu um erro ao ler o arquivo CSV: {str(e)}')

with open(output_csv, 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(coluna)
    csv_writer.writerows(data)

print(f'O arquivo formatado foi salvo como: {output_csv}')
