import requests
import os
from config import authUsername, authPassword

pattern_id = 'bear-with-scarf'
url = f'https://api.ravelry.com/patterns/{pattern_id}.json'

response = requests.get(url, auth=requests.auth.HTTPBasicAuth(authUsername, authPassword))
# print(json.dumps(json.loads(response.text), indent=4)) 

if response.status_code == 200:
    pattern_data = response.json()
    pattern = pattern_data['pattern']

    if pattern['downloadable']:
        download_location = pattern['download_location']

        if download_location['type'] == 'external':
            pdf_url = download_location['url']
            print('URL PDF:', pdf_url)
            folder_path = 'patterns'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            response = requests.get(pdf_url)
            if response.status_code == 200:
                file_path = os.path.join(folder_path, 'bear-with-scarf.pdf')

                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print('PDF успешно загружен.')
            else:
                print('Ошибка загрузки PDF:', response.text)
        else:
            print('PDF недоступен для загрузки.')
    else:
        print('Файл нельзя загрузить.')
else:
    print('Ошибка:', response.text)
