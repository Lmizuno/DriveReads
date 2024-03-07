from google.colab import auth
auth.authenticate_user()
from googleapiclient.discovery import build
drive_service = build('drive', 'v3')

import pandas as pd
data = {'Document Name': [], 'Text': []}
df = pd.DataFrame(data)

folder_id = 'put_your_folder_id_here'

# This won't apply for over 1000 files, it's the maximum, after that pagination is needed
results = drive_service.files().list(q=f"mimeType='application/vnd.google-apps.document' and '{folder_id}' in parents",
                                     pageSize=1000,
                                     fields='files(id, name)').execute()
documentsInfo = results.get('files', [])

documentsObject = []
service = build('docs', 'v1')
for document in documentsInfo:
    documentsObject.append(service.documents().get(documentId=document['id']).execute())

for document in documentsObject:
  text = ""
  for item in document['body']['content']:
    if 'paragraph' in item:
      for elements in item['paragraph']['elements']:
        text += elements['textRun']['content']
  df = df.append({'Document Name': document['title'], 'Text': text}, ignore_index=True)


spreadsheet_id = 'put_your_spreadsheet_id_here'
sheet_name = 'Sheet1'

sheets_service = build('sheets', 'v4')
body = {'values': df.values.tolist()}
write_range = f"{sheet_name}!A:Z"

try:
    sheets_service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=write_range, body=body, valueInputOption='RAW').execute()
    print("Data successfully updated in the Google Sheet.")
except Exception as e:
    print(f"Error updating data: {str(e)}")
