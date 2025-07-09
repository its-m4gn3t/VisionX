import datetime

if __name__ == '__main__':
    ftp_url = 'ftp://ftp.example.com/pub/data'  # Replace with your FTP host and path
    start_time = datetime.datetime(2020, 1, 1)
    end_time = datetime.datetime(2024, 12, 31)

    try:
        # Call walk without user/pass to use anonymous login
        files = walk(ftp_url, divby='year_month', time1=start_time, time2=end_time)
        print("Files found:")
        for f in files:
            print(f)
    except Exception as e:
        print(f"Error: {e}")
