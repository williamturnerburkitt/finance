# https://stackoverflow.com/questions/67623860/how-to-access-shared-google-drive-files-through-python
from pydrive2.auth import GoogleAuth
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.drive import GoogleDrive

auth = GoogleAuth()
auth.LocalWebserverAuth()

drive = GoogleDrive(auth)
