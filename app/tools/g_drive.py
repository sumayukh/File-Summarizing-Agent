from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

class GDriveService:
    def __init__(self, credentials):
        self.google_drive = build(serviceName="drive", version="v3", credentials=credentials)
        
    def get_folder_id(self, folder_name = "test"):
        q = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        fields = "files(id, name)"
        results = self.google_drive.files().list(q=q, fields=fields).execute()
        
        folders = results.get("files", [])
        if not folders:
            raise Exception(f"Folder '{folder_name}' not found")
        return folders[0]["id"]
    
    def list_files(self, folder_id):
        q = f"'{folder_id}' in parents"
        fields = "files(id, name, mimeType)"
        results = self.google_drive.files().list(q=q, fields=fields).execute()
        return results.get("files", [])
    
    def download_file(self, file_id, mimeType=None):
        request = self.google_drive.files().export_media(fileId=file_id, mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document") if mimeType == "application/vnd.google-apps.document" else self.google_drive.files().get_media(fileId=file_id)
        fs = io.BytesIO()
        downloader = MediaIoBaseDownload(fs, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fs.seek(0)
        return fs
        