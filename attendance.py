import csv
import os
from datetime import datetime


class AttendanceLogger:

    def __init__(self, filename="attendance.csv"):
        self.filename = filename

        # create file with header if not exists
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Date", "Time"])

        self.logged_today = set()

    # -------------------------
    # log only once per person
    # -------------------------
    def log(self, name):

        today = datetime.now().strftime("%Y-%m-%d")

        key = f"{name}-{today}"

        # prevent duplicate entries
        if key in self.logged_today:
            return

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, date, time])

        self.logged_today.add(key)

        print(f"✅ Attendance marked for {name}")
