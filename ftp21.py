import ftplib
import os

class FTPClient:
    def __init__(self, host, username='anonymous', password='anonymous@domain.com', port=21):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ftp = ftplib.FTP()
    
    def connect(self):
        print(f"Connecting to {self.host}:{self.port}...")
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.username, self.password)
        print(f"Logged in as {self.username}")
    
    def list_files(self, path='.'):
        print(f"Listing files in {path}:")
        self.ftp.cwd(path)
        files = self.ftp.nlst()
        for f in files:
            print(f" - {f}")
        return files
    
    def download_file(self, remote_file, local_file=None):
        if not local_file:
            local_file = remote_file
        print(f"Downloading {remote_file} to {local_file}...")
        with open(local_file, 'wb') as f:
            self.ftp.retrbinary(f'RETR {remote_file}', f.write)
        print("Download complete.")
    
    def upload_file(self, local_file, remote_file=None):
        if not remote_file:
            remote_file = os.path.basename(local_file)
        print(f"Uploading {local_file} to {remote_file}...")
        with open(local_file, 'rb') as f:
            self.ftp.storbinary(f'STOR {remote_file}', f)
        print("Upload complete.")
    
    def upload_directory(self, local_dir, remote_dir):
        print(f"Uploading directory {local_dir} to {remote_dir} recursively...")
        try:
            self.ftp.mkd(remote_dir)
            print(f"Created directory {remote_dir}")
        except ftplib.error_perm:
            print(f"Directory {remote_dir} already exists")
        self.ftp.cwd(remote_dir)
        for root, dirs, files in os.walk(local_dir):
            rel_path = os.path.relpath(root, local_dir)
            if rel_path != '.':
                try:
                    self.ftp.mkd(rel_path)
                    print(f"Created directory {rel_path}")
                except ftplib.error_perm:
                    print(f"Directory {rel_path} already exists")
                self.ftp.cwd(rel_path)
            for file in files:
                local_path = os.path.join(root, file)
                self.upload_file(local_path, file)
            # Move back to remote_dir root after uploading each subdirectory
            if rel_path != '.':
                self.ftp.cwd(remote_dir)
        print("Directory upload complete.")
    
    def close(self):
        self.ftp.quit()
        print("Connection closed.")

# Example usage
if __name__ == "__main__":
    ftp_host = '169.154.154.63'
    ftp_user = 'anonymous'  # or your username
    ftp_pass = 'your-email@example.com'  # or your password

    client = FTPClient(ftp_host, ftp_user, ftp_pass)
    client.connect()
    
    # List files in root directory
    client.list_files('/')
    
    # Download a file
    client.download_file('remote_filename.txt')
    
    # Upload a single file
    client.upload_file('local_filename.txt')
    
    # Upload a directory recursively
    client.upload_directory('/path/to/local/dir', '/remote/dir')
    
    client.close()
