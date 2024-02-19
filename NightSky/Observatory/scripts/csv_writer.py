from djqscsv import write_csv


class CsvWriter:
    def __init__(self, queryset):
        self.queryset = queryset

    def write(self, path):
        with open(path + '/metadata.csv', 'wb') as csv_file:
            write_csv(self.queryset, csv_file)