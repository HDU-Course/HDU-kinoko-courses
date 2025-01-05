#!/usr/bin/env python3
# ftp test

from ftplib import FTP
import time
import os
import tarfile

from ftplib import FTP

def ftpconnect(host, username, password):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    ftp.cwd("/")
    return ftp

def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.set_debuglevel(2)
    ftp.retrbinary('RETR '+remotepath, fp.write, bufsize)
    fp.close()

def uploadfile(ftp, remotepath, localpath):
    if os.path.isfile(localpath) == False:
        print("Error when uploading!")
        return False
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.set_debuglevel(2)
    ftp.storbinary('STOR '+remotepath, fp, bufsize)
    fp.close()

if __name__ == '__main__':
    #ftp = ftpconnect("172.104.104.179", "biosec", "hdu-study")
    ftp = ftpconnect("v1.ftp.upyun.com", "hdu/hezuo-hdu", "2017_11-20_hezuo*#")
    downloadfile(ftp, "test.txt", "/Users/Wintone/Desktop/test_downloaded.txt")
    uploadfile(ftp, "test_uploaded.txt", "/Users/Wintone/Desktop/test.txt")

    ftp.quit()
