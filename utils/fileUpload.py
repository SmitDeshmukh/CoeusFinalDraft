import requests

def getFileUploadLink(file):
    site = 'https://asia-south1-coeus-1482f.cloudfunctions.net/api/upload-file'
    up = {'file':(file.name, file.read(), "multipart/form-data")}
    resp = requests.post(site, files=up).json()
    return resp['link']