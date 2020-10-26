import io
import pandas as pd


def generate_csv(items, fields, delimiter=','):
    rows = ''
    # add header
    header_data = delimiter.join(map(str, fields))
    rows += f'{header_data}\n'
    # add items
    for item in items:
        # create item record
        fields_values = []
        for field in fields:
            # getting specific field from item
            fields_values.append(str(item.get(field) or ''))
        row_data = delimiter.join(fields_values)
        rows += f'{row_data}\n'
    return rows


def parse_df(df, fields: list):
    keys = df.keys()

    df_to_model_keys = dict(zip(keys, fields))
    df = df.rename(columns=df_to_model_keys)
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient='records')

def read_dataframe(path):
    with open(path, 'rb') as file:
        ext = file.name.split('.')[-1]
        # can be used in future
        df = None
        extra = dict()
        if ext == 'csv':
            df = pd.read_csv(file, **extra)
        elif ext == 'tsv':
            df = pd.read_csv(file, sep="\t", **extra)
        elif ext in ['xls', 'xlsx']:
            df = pd.read_excel(file, sheet_name=0, **extra)
        elif ext == 'ods':
            df = pd.read_excel(file, sheet_name=0, engine='odf', **extra)

        return df


def parse_bulk_file(file, fields):
    df = read_dataframe(file)
    return parse_df(df, fields)
