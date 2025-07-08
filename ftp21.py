import socket
import ftplib
import argparse
import json

def is_ftp_open(host, port=21, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            banner = sock.recv(1024).decode(errors='ignore').strip()
            return True, banner
    except Exception:
        return False, None

def check_ftp_anonymous_login(host, timeout=5):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, 21, timeout=timeout)
        ftp.login()  # Attempts anonymous login by default
        files = ftp.nlst()
        ftp.quit()
        return True, files
    except ftplib.error_perm as e:
        return False, str(e)
    except Exception:
        return False, None

def scan_host(host):
    print(f"[*] Scanning {host}...")
    result = {
        "host": host,
        "ftp_open": False,
        "banner": None,
        "anonymous_login": False,
        "file_list": None
    }

    is_open, banner = is_ftp_open(host)
    if not is_open:
        return result

    result["ftp_open"] = True
    result["banner"] = banner

    anon_login, data = check_ftp_anonymous_login(host)
    result["anonymous_login"] = anon_login
    result["file_list"] = data if anon_login else None

    return result

def main():
    parser = argparse.ArgumentParser(description="FTP Security Scanner")
    parser.add_argument("targets", help="IP address, domain, or path to file containing targets")
    parser.add_argument("-o", "--output", help="Save output to JSON file")
    args = parser.parse_args()

    hosts = []

    # Load targets from file or use single input
    try:
        with open(args.targets, "r") as f:
            hosts = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        hosts = [args.targets]

    results = []

    for host in hosts:
        result = scan_host(host)
        results.append(result)
        print(json.dumps(result, indent=2))

    if args.output:
        with open(args.output, "w") as out:
            json.dump(results, out, indent=2)
        print(f"[+] Results saved to {args.output}")

if __name__ == "__main__":
    main()
