googleDriveAccess
=================

a Python tool to Access to the Google Drive ( OAuth2, Calendar, Gmail, etc )

Package Documentation https://github.com/HatsuneMiku/googleDriveAccess/wiki/module_googleDriveAccess


Sample
------

``` python
import os
import googleDriveAccess as gda

# create instance
da = gda.DAClient(os.path.abspath('.'))

# create parent folders at the same time
folderId, folderPath = da.makeDirs('/remote_drive/subfolder_test/subsubfolder')
print folderId, folderPath

# recursive backup to remote folder
da.recursiveUpload('a_local_directory_you_want_to_backup_recursively')

# search
da.execQuery("explicitlyTrashed=True")
da.execQuery("'root' in parents", **{'maxResults': 5})
da.execQuery("'root' in parents and explicitlyTrashed=True", repeattoken=True, **{'maxResults': 500})

# OAuth2
oa2 = gda.OAuth2Client(abc=da)
ui = oa2.userInfo()
act = ui['email']
print act

# gmail
gm = gda.GmailClient(abc=oa2)
mo = gm.sendMsg(act, act, 'message title', 'message text')
if mo:
  mo = gm.modifyLabels(mo['id'], addLabels=['INBOX', 'UNREAD', 'STARRED'])
mo = gm.sendMsg(act, act, 'title attach', 'text attach', 'test_document.txt')
if mo:
  mo = gm.modifyLabels(mo['id'], addLabels=['INBOX', 'UNREAD', 'STARRED'])

# calendar
import time
ca = gda.CalendarClient('Asia/Tokyo', abc=oa2)
cals = ca.idList()
for cal in cals['items']:
  print u'%s : %s' % (cal['id'], cal['summary']) # unicode
id = cals['items'][0]['id']
print id
TEST_TITLE = u'今日の待ち合わせ' # unicode
t = time.time()
eo = ca.insertEvent(id,
  start=ca.isoDate(t), end=ca.isoDate(t + 24 * 3600), # date only
  location=u'皇居', summary=TEST_TITLE) # unicode
eo = ca.insertEvent(id,
  start=ca.isoTime(t + 1800), end=ca.isoTime(t + 3600), # date and time
  location=u'京都御所', summary=TEST_TITLE) # unicode
```


How to use it
-------------

Install

``` bash
pip install 'google-api-python-client'
pip install googleDriveAccess
  (or easy_install googleDriveAccess)
cd /opt/googleDriveAccess
```


First, create your Client_ID and secret on the Google Drive.

Register your App on https://console.developers.google.com/project
and *'download JSON'* of your Client ID and Client secret.

Rename this JSON file to './client_secret_[Client ID].json' .

``` bash
mv client_secrets.json /opt/googleDriveAccess/client_secret_YOURCLIENTID.json
```


Second, create cache file for Client ID .

Create './cicache.txt' file and write your Client ID to the first line.

``` bash
echo YOURCLIENTID > ./cicache.txt
```


Third, encrypt secret file.

Execute ./encrypt_client_secret.py to encrypt downloaded JSON file.

``` bash
./encrypt_client_secret.py
```


Check that encrypted file exists './client_secret_[Client ID].json.enc'
and plain text JSON file './client_secret_[Client ID].json' will be deleted.

Execute ./test_upload_first.py to test OAuth2 flow and store credentials.

``` bash
./test_upload_first.py
```


Execute ./test_upload_second.py to test OAuth2 using stored credentials.

``` bash
./test_upload_second.py
```


Execute ./test_calendar_v3.py to test OAuth2 and add calendar event.

``` bash
./test_calendar_v3.py
```


Execute ./test_gmail_v1.py to test OAuth2 and send mail and modify labels.

``` bash
./test_gmail_v1.py
```


Execute ./test_script_prefetch.py to test Drive API search with query.

``` bash
./test_script_prefetch.py
```


Edit test_script_import_export.py (set 'mode = 0')
to test create new Google Apps Script
'test_GoogleAppsScript_createCalendarEvent' for tests below.

Execute ./test_script_import_export.py to test create and *'get SCRIPT_ID'* .

``` bash
./test_script_import_export.py
```


Edit test_script_import_export.py (set 'mode = 2' and *'set SCRIPT_ID'*)
to test download.

Execute ./test_script_import_export.py to test download.

``` bash
./test_script_import_export.py
```


Edit downloaded script
'./script_import_export/test_GoogleAppsScript_createCalendarEvent/Code.gs' .

Edit test_script_import_export.py (set 'mode = 1') to test upload.

Execute ./test_script_import_export.py to test upload.

``` bash
./test_script_import_export.py
```


Known BUGs
----------

Fails to create and update Google Apps Script.

```
mimeType was changed about specification of uploading Google Apps Script ?
```


I will make refresh_cache.py :

```
This program will cache each folder (or file) ids assigned by the Google Drive.
(Into the cache file cache_folderIds_[Client ID]_[OAuth2Act].sl3 .)
Please search and erase a row that has same id from the cache file
when you delete your folder or file using another Google Drive client tool.
```


It may be fixed:

```
When uploading a file that would not be automaticaly handled Google Drive,
"Media type 'None' is not supported. Valid media types: [*/*]"
error occurred.
Because of default mimeType is set to None on uploadFile.
So it may correct to catch the exception and retry with 'binary/octet-stream'.
```


Links
-----

Package Documentation https://github.com/HatsuneMiku/googleDriveAccess/wiki/module_googleDriveAccess

You can get the latest version at this GitHub repository.
https://github.com/HatsuneMiku/googleDriveAccess

GitHub HomePage http://hatsunemiku.github.io/googleDriveAccess

PyPI https://pypi.python.org/pypi/googleDriveAccess


Relations
---------

pytz-memcache https://github.com/HatsuneMiku/pytz-memcache

pytz-memcache (PyPI) https://pypi.python.org/pypi/pytz-memcache


License
-------

BSD License

