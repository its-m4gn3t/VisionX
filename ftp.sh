#!/bin/bash

# FTP server IP
FTP_HOST="169.154.154.63"

# FTP login credentials (anonymous)
FTP_USER="anonymous"
FTP_PASS="anonymous@domain.com"

# Remote file path on FTP server
REMOTE_FILE="/path/to/remote/file.txt"

# Local destination path on your laptop
LOCAL_DEST="./file.txt"

echo "Connecting to FTP server $FTP_HOST and downloading $REMOTE_FILE..."

ftp -inv $FTP_HOST <<EOF
user $FTP_USER $FTP_PASS
binary
get $REMOTE_FILE $LOCAL_DEST
bye
EOF

echo "Download completed. File saved to $LOCAL_DEST"
