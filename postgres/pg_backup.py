import os
from sh import pg_dump


def createFolder(session):
    metadata = {
        'name': datetime.datetime.utcnow().isoformat(),
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [os.getenv('GDRIVE_ROOT_FOLDER_ID')]
    }
    response = session.post(
        'https://www.googleapis.com/drive/v3/files?supportsAllDrives=true',
        json=metadata
    )
    response.raise_for_status()
    return response.json()['id']


def upload(name, session, folderId, mimeType):
    file_metadata = {
        'name': name,
        'mimeType': mimeType,
        'parents': [folderId]
    }
    start_response = session.post(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true',
        json=file_metadata
    )
    start_response.raise_for_status()
    resumable_uri = start_response.headers.get('Location')
    file = open('backup/{}'.format(name), 'rb')
    upload_response = session.put(resumable_uri, data=file)
    upload_response.raise_for_status()

def main():
    with open('backup.psql', 'wb') as f:
        pg_dump('--dbname', os.getenv('PG_CONNECTION'), _out=f)

    service_account_info = json.loads(os.getenv('GDRIVE_SERVICE_ACCOUNT'))
    google_credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    authed_session = AuthorizedSession(google_credentials)
    folderId = createFolder(authed_session)
    upload('backup.psql', authed_session, folderId, 'application/zip')


if __name__ == "__main__":
    main()
