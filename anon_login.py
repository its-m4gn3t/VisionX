import os
from ftplib import FTP_TLS

def ftps_anonymous_upload_test(host):
    test_filename = 'poc_test_file.txt'
    test_content = 'PoC file for anonymous FTPS upload permission testing.\n'

    # Create a local test file
    with open(test_filename, 'w') as f:
        f.write(test_content)

    try:
        print(f"[+] Connecting to FTPS server {host} as anonymous user...")
        ftps = FTP_TLS(host, timeout=10)
        ftps.login(user='anonymous', passwd='anonymous')
        print("[+] Anonymous FTPS login successful.")

        # Secure the data connection
        ftps.prot_p()

        print("[*] Directory listing before upload:")
        ftps.retrlines('LIST')

        # Attempt to upload the test file
        with open(test_filename, 'rb') as f:
            print(f"[+] Attempting to upload test file '{test_filename}'...")
            ftps.storbinary(f'STOR {test_filename}', f)
        print("[+] Upload succeeded. Server allows anonymous write access — potential security risk!")

        print("[*] Directory listing after upload:")
        lines = []
        ftps.retrlines('LIST', lines.append)

        # Search for uploaded file in directory listing and print details
        file_info = next((line for line in lines if test_filename in line), None)
        if file_info:
            print(f"[+] Uploaded file details:\n{file_info}")
        else:
            print("[!] Uploaded file not found in directory listing — possible delay or permission issue.")

        # Cleanup: delete the uploaded test file
        try:
            ftps.delete(test_filename)
            print(f"[+] Uploaded file '{test_filename}' deleted successfully.")
        except Exception as del_err:
            print(f"[!] Could not delete uploaded file: {del_err} — manual cleanup may be required.")

        ftps.quit()
        print("[+] FTPS session closed.")

    except Exception as e:
        print(f"[!] Error during FTPS testing: {e}")

    finally:
        # Remove local test file
        if os.path.exists(test_filename):
            os.remove(test_filename)
            print("[*] Local test file removed.")

if __name__ == "__main__":
    target_ip = '169.154.154.63'  # Replace with your target FTP server IP or hostname
    ftps_anonymous_upload_test(target_ip)
