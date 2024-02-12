from astropy.time import Time
import csv
import os
import pandas as pd
from .parse_for_log import ParseForLog


class Log:
    def __init__(self, headers, path):
        self.num = 1
        self.COLUMNS = 15
        self.rows = [["AGO 0.7m observation log"] + [""] * self.COLUMNS]
        self.headers = headers
        self.path = path

        self.NAMES = ["Observer", "Date", "CCD Temp", "Weather", "Moon", "Remark"]
        self.HEADER = [
            "",
            "Expected Product",
            "Object name",
            "Series no.",
            "Time (UTC)",
            "Filter",
            "Dimension",
            "Exposure",
            "Delay",
            "N",
            "Tracking Type",
            "NORAD",
            "Object Type",
            "Orbit Type",
            "Comment",
        ]

        self.series_counts = {}
        self.date = None

    def generate_log(self):
        self.make_header()
        self.fill_log()
        self.add_column_n()
        self.write()

    def make_header(self):
        for name in self.NAMES:
            row = [name + ":", ""]
            self.rows.append(row)
        self.rows.append(self.HEADER)
        self.add_data_to_header()

    def fill_log(self):
        for header in self.headers:
            log_row = ParseForLog(header, self.num)
            if log_row.has_header():
                log_row.add_data()
                self.rows.append(log_row.get_data())
                self.add_to_series_counts(log_row)
                self.num += 1

    def add_data_to_header(self):
        log_row = self.pick_one_fits()
        if log_row is None:
            return
        self.rows[1][1] = log_row.get_value_of("OBSERVER")

        date_obs = Time(log_row.get_value_of("DATE-OBS"), format="fits")
        self.date = date_obs.datetime.strftime("%Y-%m-%d")
        self.rows[2][1] = self.date

        self.rows[3][1] = log_row.get_value_of("CCD-TEMP")

    def pick_one_fits(self):
        if self.headers:
            for image in self.headers:
                if "T" in image["DATE-OBS"]:
                    return ParseForLog(image, self.num)
        return None

    def add_to_series_counts(self, log_row):
        key = log_row.get_data_for_n()
        try:
            self.series_counts[key] += 1
        except KeyError:
            self.series_counts[key] = 1

    def add_column_n(self):
        for row in self.rows[8:]:
            if isinstance(row, list) and len(row) >= 5:
                n = self.series_counts[(row[2], row[3], row[5])]
                row.append(n)

    def write(self):
        name = self.path + "/AGO_Log_" + self.date + ".csv"
        with open(name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerows(self.rows)
        # convert csv to xlsx:
        csv_file = pd.read_csv(name, header=None)
        csv_file.to_excel(self.path + "/AGO_Log_excel_" + self.date + ".xlsx", index=False, header=False)
