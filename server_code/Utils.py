import anvil.server
import anvil.media

from datetime import date, datetime
import pandas as pd


def convert_dict_ts_to_isoformat(d: dict) -> dict:
    new_dict = d.copy()
    for v in new_dict.values():
        if isinstance(v, datetime) or isinstance(v, date):
            v = v.isoformat()
    return new_dict


def get_spreadsheet_records(file) -> list[dict]:  # might want to double-check this return type
    with anvil.media.TempFile(file) as f:
        if file.content_type == 'text/csv':
            df = pd.read_csv(f, header=None)
        else:
            df = pd.read_excel(f, header=None)
    return df.to_dict('records')
