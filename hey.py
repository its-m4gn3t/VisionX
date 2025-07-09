import os
from ftplib import FTP_TLS

def ftps_login_and_download_all(host):
    try:
        # Get user credentials
        uname = input("Enter FTP username (or 'anonymous'): ")
        passwd = input("Enter FTP password (or 'anonymous'): ")

        print(f"[+] Connecting to FTPS server {host}...")
        ftps = FTP_TLS(host, timeout=10)
        ftps.login(user=uname, passwd=passwd)
        print("[+] FTPS login successful.")

        # Secure the data connection
        ftps.prot_p()

        print("[*] Directory listing:")
        files = []
        ftps.retrlines('LIST', files.append)
        for line in files:
            print(line)

        # Extract filenames from the directory listing
        # Assuming standard UNIX-like LIST format, filename is last token
        filenames = [line.split()[-1] for line in files if line.startswith('-')]

        if not filenames:
            print("[!] No files found to download.")
        else:
            print(f"[*] Found {len(filenames)} files. Starting download...")

            for filename in filenames:
                local_filename = os.path.join('.', filename)
                with open(local_filename, 'wb') as f:
                    print(f"[+] Downloading {filename}...")
                    ftps.retrbinary(f'RETR {filename}', f.write)
                print(f"[+] Downloaded {filename} successfully.")

        ftps.quit()
        print("[+] FTPS session closed.")

    except Exception as e:
        print(f"[!] Error during FTPS operation: {e}")

if __name__ == "__main__":
    target_ip = '169.154.154.63'  # Replace with your target FTP server IP or hostname
    ftps_login_and_download_all(target_ip)
