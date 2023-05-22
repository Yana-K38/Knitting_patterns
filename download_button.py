import requests
import os
import json
from config import authUsername, authPassword

pattern_id = 'cat-pack-attack-vol-1'

pattern_url = f'https://api.ravelry.com/patterns/{pattern_id}.json'

response = requests.get(pattern_url, auth=requests.auth.HTTPBasicAuth(authUsername, authPassword))
pattern_data = response.json()

if response.status_code == 200:
    pattern = pattern_data['pattern']
    if pattern['downloadable']:
        download_location = pattern['download_location']

        if download_location['type'] == 'ravelry':
            pdf_url = download_location['url']
            print('URL PDF:', pdf_url)

            pdf_response = requests.get(pdf_url)
            print(pdf_response.text)
            if pdf_response.status_code == 200:
                folder_path = 'patterns'
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, f'{pattern_id}.pdf')

                with open(file_path, 'wb') as file:
                    file.write(pdf_response.content)
                print('PDF успешно загружен.')
            else:
                print('Ошибка загрузки PDF:', pdf_response.text)
        else:
            print('PDF недоступен для загрузки.')
    else:
        print('Файл нельзя загрузить.')
else:
    print('Ошибка:', response.text)