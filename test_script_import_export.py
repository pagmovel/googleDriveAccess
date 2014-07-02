#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''test_script_import_export
OAuth2 'credentials_CI.json.enc'
Apps Script Crash Course: Import/Export Apps Script Code
https://www.youtube.com/watch?v=lEVMu9KE6jk
Google Drive SDK: Searching for files
https://www.youtube.com/watch?v=DOSvQmQK_HA
https://developers.google.com/drive/v2/reference/files/list
GET https://www.googleapis.com/drive/v2/files?key={YOUR_API_KEY}
GET https://www.googleapis.com/drive/v2/files?q=mimeTyep%3D%27application%2Fvnd.google-apps.script%27&key={YOUR_API_KEY}
GET https://www.googleapis.com/drive/v2/files?q=mimeTyep%3D%27application%2Fvnd.google-apps.spreadsheet%27&key={YOUR_API_KEY}
import: upload
export: download
'''

import sys, os
import socket
import pprint

from apiclient.http import MediaFileUpload
from oauth2client.anyjson import simplejson
import googleDriveAccess

import logging
logging.basicConfig()
logger = logging.getLogger()

MANIFEST = 'manifest.json'
SCRIPT_TYPE = 'application/vnd.google-apps.script+json'
SCRIPT_FOLDER = 'script_import_export'
SCRIPT_ID = 'SCRIPT_ID_YOU_WISH_TO_HANDLE'
SCRIPT_NAME = 'SCRIPT_NAME_YOU_WISH_TO_HANDLE'

def script_upload(drive_service, basedir, folder, id, name):
  foldername = os.path.join(basedir, folder, name)
  logger.info('prepare folder: %s' % foldername)
  manifest_path = os.path.join(foldername, MANIFEST)
  mfile = open(manifest_path, 'rb')
  data = simplejson.loads(mfile.read())
  mfile.close()
  # import files in the directory
  for i, fileInProject in enumerate(data['files']):
    extension = '.html' # default
    if fileInProject['type'] == 'server_js': extension = '.gs'
    filename = '%s%s' % (fileInProject['name'], extension)
    logger.info('- file%04d: %s' % (i, filename))
    f = open(os.path.join(foldername, filename), 'rb')
    fileInProject['source'] = f.read()
    f.close()
  # last import manifest.json
  logger.info('- manifest: %s' % MANIFEST)
  mfile = open(manifest_path, 'wb')
  mfile.write(simplejson.dumps(data))
  mfile.close()

  # body = {'title': name, 'mimeType': SCRIPT_TYPE, 'description': name}
  body = {'mimeType': SCRIPT_TYPE}
  mbody = MediaFileUpload(manifest_path, mimetype=SCRIPT_TYPE, resumable=True)
  if False: # create new Apps Script project
    fileobj = drive_service.files().insert(
      body=body, media_body=mbody).execute()
  else: # overwrite exists Apps Script project
    fileobj = drive_service.files().update(
      fileId=id, body=body, media_body=mbody).execute()
  pprint.pprint(fileobj)

def script_download(drive_service, basedir, folder, id):
  fileobj = drive_service.files().get(fileId=id).execute()
  download_url = fileobj['exportLinks'][SCRIPT_TYPE]
  resp, content = drive_service._http.request(download_url)
  if resp.status != 200: raise Exception('An error occurred: %s' % resp)
  data = simplejson.loads(content)
  foldername = os.path.join(basedir, folder, fileobj['title'])
  logger.info('prepare folder: %s' % foldername)
  if not os.path.exists(foldername): os.makedirs(foldername)
  # Delete any files in the directory
  for the_file in os.listdir(foldername):
    file_path = os.path.join(foldername, the_file)
    try:
      if os.path.isfile(file_path): os.unlink(file_path)
    except (Exception, ), e:
      print e
  # first export manifest.json
  manifest_path = os.path.join(foldername, MANIFEST)
  logger.info('- manifest: %s' % MANIFEST)
  mfile = open(manifest_path, 'wb')
  mfile.write(content)
  mfile.close()
  # export files in the directory
  for i, fileInProject in enumerate(data['files']):
    extension = '.html' # default
    if fileInProject['type'] == 'server_js': extension = '.gs'
    filename = '%s%s' % (fileInProject['name'], extension)
    logger.info('- file%04d: %s' % (i, filename))
    f = open(os.path.join(foldername, filename), 'wb')
    f.write(fileInProject['source'])
    f.close()

def main(basedir):
  ci = googleDriveAccess.readClientId(basedir)
  drive_service = googleDriveAccess.second_authorize(basedir, ci, script=True)
  #script_upload(drive_service, basedir, SCRIPT_FOLDER, SCRIPT_ID, SCRIPT_NAME)
  script_download(drive_service, basedir, SCRIPT_FOLDER, SCRIPT_ID)

if __name__ == '__main__':
  logging.getLogger().setLevel(getattr(logging, 'INFO')) # ERROR
  try:
    main(os.path.dirname(__file__))
  except (socket.gaierror, ), e:
    sys.stderr.write('socket.gaierror')