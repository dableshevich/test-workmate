import argparse

from app.csv_data import CSVData


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Путь к файлу')
    parser.add_argument('--where', help='Фильтрация данных')
    parser.add_argument('--aggregate', help='Агрегирование данных')

    args = parser.parse_args()

    csv_data = CSVData(args.file)
    if args.where:
        csv_data.filter(args.where)
    if args.aggregate:
        csv_data.aggregate(args.aggregate)
    csv_data.print()


if __name__ == '__main__':
    main()
