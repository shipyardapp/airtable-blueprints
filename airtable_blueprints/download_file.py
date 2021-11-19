from pyairtable import Base, Table
import os
import argparse
import pandas as pd
import code


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--base-id',
        dest='base_id',
        default='',
        required=True)
    parser.add_argument(
        '--table-name',
        dest='table_name',
        default=None,
        required=True)
    parser.add_argument(
        '--view-name',
        dest='view_name',
        default=None,
        required=False)
    parser.add_argument(
        '--destination-file-name',
        dest='destination_file_name',
        default=None,
        required=True)
    parser.add_argument(
        '--destination-folder-name',
        dest='destination_folder_name',
        default='',
        required=False)
    parser.add_argument(
        '--cell-range',
        dest='cell_range',
        default='A1:ZZZ5000000',
        required=False)
    parser.add_argument(
        '--api-key',
        dest='api_key',
        default=None,
        required=True)
    parser.add_argument(
        '--include-record-id',
        dest='include_record_id',
        choices={
            'TRUE',
            'FALSE'},
        default='TRUE',
        required=False)
    return parser.parse_args()


def clean_folder_name(folder_name):
    """
    Cleans folders name by removing duplicate '/' as well as leading and trailing '/' characters.
    """
    folder_name = folder_name.strip('/')
    if folder_name != '':
        folder_name = os.path.normpath(folder_name)
    return folder_name


def combine_folder_and_file_name(folder_name, file_name):
    """
    Combine together the provided folder_name and file_name into one path variable.
    """
    combined_name = os.path.normpath(
        f'{folder_name}{"/" if folder_name else ""}{file_name}')

    return combined_name


def convert_to_boolean(string):
    """
    Shipyard can't support passing Booleans to code, so we have to convert
    string values to their boolean values.
    """
    if string in ['True', 'true', 'TRUE']:
        value = True
    else:
        value = False
    return value


def main():
    args = get_args()
    api_key = args.api_key
    table_name = args.table_name
    base_id = args.base_id
    view_name = args.view_name
    include_record_id = convert_to_boolean(args.include_record_id)
    destination_file_name = clean_folder_name(args.destination_file_name)
    destination_folder_name = clean_folder_name(args.destination_folder_name)

    destination_full_path = combine_folder_and_file_name(
        folder_name=destination_folder_name, file_name=destination_file_name)
    if not os.path.exists(destination_folder_name) and \
            (destination_folder_name != ''):
        os.makedirs(destination_folder_name)

    code.interact(local=locals())
    table = Table(api_key, base_id, table_name)
    records = table.all(view=view_name)

    df = pd.DataFrame.from_records(row['fields'] for row in records)

    if include_record_id:
        for index, row in enumerate(records):
            df.at[index, 'airtable_record_id'] = row['id']

    df.to_csv(destination_full_path, index=False)


if __name__ == '__main__':
    main()