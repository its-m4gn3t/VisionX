import ftplib
import re
import datetime
from fnmatch import fnmatch
from urllib.parse import urlparse
from typing import List, Tuple, Optional

SKIPPATS = ['.', '..']

def walk(full_path: str,
         divby: str = 'none',
         time1: datetime.datetime = datetime.datetime.min,
         time2: datetime.datetime = datetime.datetime.max,
         user: Optional[str] = None,
         passwd: Optional[str] = None) -> List[str]:
    """
    Walk an FTP directory tree and return a list of file paths.

    Args:
        full_path: FTP URL, e.g. 'ftp://ftp.example.com/path/to/dir'
        divby: underscore-separated hierarchy filters (e.g. 'year_month')
        time1: start datetime for filtering directories by name
        time2: end datetime for filtering directories by name
        user: FTP username (default: anonymous)
        passwd: FTP password (default: anonymous)

    Returns:
        List of file paths matching criteria.
    """
    parts = urlparse(full_path)
    protocol, siteadd, basedir = parts.scheme, parts.hostname, parts.path
    if protocol != 'ftp':
        raise ValueError("Only FTP protocol is supported")

    divisions = divby.split('_') if divby else ['none']

    ftp = ftplib.FTP(siteadd)
    try:
        if user and passwd:
            ftp.login(user=user, passwd=passwd)
        else:
            ftp.login()  # anonymous login
    except ftplib.all_errors as e:
        raise ConnectionError(f"FTP login failed: {e}")

    try:
        stats = ftp.sendcmd('STAT')
    except ftplib.error_perm:
        stats = ''

    if 'Microsoft' in stats:
        servertype = 'microsoft'
    elif 'Mac' in stats:
        servertype = 'mac'
    elif 'MultiNet FTP Server' in stats:
        servertype = 'vms'
    else:
        servertype = 'unix'

    try:
        ftp.cwd(basedir)
    except ftplib.error_perm:
        ftp.quit()
        raise FileNotFoundError(f"Data directory '{basedir}' does not exist on remote server!")

    results = walkftp(ftp, servertype, divisions, time1, time2)

    ftp.quit()
    return results


def walkftp(ftp: ftplib.FTP,
            servertype: str,
            divby: List[str],
            time1: datetime.datetime,
            time2: datetime.datetime) -> List[str]:
    """
    Recursively walk FTP directories and collect file paths.

    Args:
        ftp: active FTP connection
        servertype: server listing type ('unix', 'microsoft', 'mac', etc.)
        divby: list of directory filters (e.g., ['year', 'month'])
        time1: start datetime filter
        time2: end datetime filter

    Returns:
        List of file paths.
    """
    results = []
    pwd = ftp.pwd()
    subdirs, filesfound = getdirlisting(ftp, servertype)

    # If at bottom directory level, add files
    if divby[0] == 'none':
        results.extend(f"{pwd}/{filename}" for filename in filesfound)
    else:
        for subdir in subdirs:
            try:
                ftp.cwd(f"{pwd}/{subdir}")
            except ftplib.error_perm as e:
                print(f"Can't change directory to {subdir}: {e}")
                continue

            # Apply time-based filtering if applicable
            if divby[0] == 'year':
                try:
                    year = int(subdir)
                    if time1.year - 1 <= year <= time2.year:
                        results.extend(walkftp(ftp, servertype, divby[1:], time1, time2))
                except ValueError:
                    # Directory name is not an integer year, skip
                    pass
            elif divby[0] == 'month':
                try:
                    month = int(subdir)
                    if 1 <= month <= 12:
                        # Optionally, you can check if the month is within time1 and time2 range
                        results.extend(walkftp(ftp, servertype, divby[1:], time1, time2))
                except ValueError:
                    pass
            else:
                # No special filtering, just recurse
                results.extend(walkftp(ftp, servertype, divby[1:], time1, time2))

            ftp.cwd(pwd)  # Go back to parent directory

    return results


def getdirlisting(ftp: ftplib.FTP, servertype: str = 'unix') -> Tuple[List[str], List[str]]:
    """
    Get subdirectories and files from current FTP directory.

    Args:
        ftp: active FTP connection
        servertype: type of FTP server listing format

    Returns:
        Tuple of (subdirectories, files)
    """
    subdirs = []
    files = []
    info = {}
    listing = []

    ftp.retrlines('LIST', listing.append)

    for line in listing:
        if servertype == 'mac':
            filename = line.strip()
            mode = 'd' if filename.endswith('/') else '-'
            if mode == 'd':
                filename = filename[:-1]
            infostuff = ''
        elif servertype == 'microsoft':
            words = line.split(None, 3)
            if len(words) < 4:
                continue
            filename = words[-1].lstrip()
            mode = 'd' if words[-2] == '<DIR>' else '-'
            infostuff = words[:-2]
        else:
            # Default to UNIX style parsing
            words = line.split(None, 8)
            if len(words) < 6:
                continue
            filename = words[-1].lstrip()
            if ' -> ' in filename:
                filename = filename.split(' -> ')[0]
            mode = words[0]
            infostuff = words[-5:-1]

        # Skip unwanted names
        if any(fnmatch(filename, pat) for pat in SKIPPATS):
            continue

        if mode.startswith('d'):
            subdirs.append(filename)
        else:
            # Avoid duplicates with same info
            if filename not in info or info[filename] != infostuff:
                files.append(filename)
                info[filename] = infostuff

    return subdirs, files


if __name__ == '__main__':
    # Example usage
    ftp_url = 'ftp://ftp.example.com/pub/data'
    start_time = datetime.datetime(2020, 1, 1)
    end_time = datetime.datetime(2024, 12, 31)
    try:
        files = walk(ftp_url, divby='year_month', time1=start_time, time2=end_time)
        print("Files found:")
        for f in files:
            print(f)
    except Exception as e:
        print(f"Error: {e}")
