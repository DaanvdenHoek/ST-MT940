from io import BytesIO
import re
import pandas as pd
import mt940
from src.options import OutputOption


def parse_mt940(file: BytesIO) -> pd.DataFrame:
    transactions = mt940.parse(file)
    data = [t.data for t in transactions]
    df = pd.DataFrame.from_records(data)
    df["amount"] = pd.to_numeric(df["amount"].map(lambda x: x.amount))
    df["date"] = pd.to_datetime(df["date"])
    return df


def clean_sheet_name(name: str) -> str:
    name = re.sub(r"[\\/*?:[\]]", "_", name)  # remove invalid Excel chars
    return name[:31] or "Sheet"


def export_multi_sheet(dfs: list[pd.DataFrame], file_names: list[str]) -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:  # type: ignore
        for df, name in zip(dfs, file_names):
            sheet_name = clean_sheet_name(name)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output


def export_single_sheet(dfs: list[pd.DataFrame], file_names: list[str]) -> BytesIO:
    df = pd.concat(df.copy().assign(file=name) for df, name in zip(dfs, file_names))
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:  # type: ignore
        df.to_excel(writer, sheet_name="Transactions", index=False)
    output.seek(0)
    return output


def df_to_xlsx_bytes(
    dfs: list[pd.DataFrame], file_names: list[str], processing_option: OutputOption
) -> BytesIO:
    if processing_option == OutputOption.SINGLE_SHEET:
        return export_single_sheet(dfs, file_names)
    elif processing_option == OutputOption.MULTI_SHEET:
        return export_multi_sheet(dfs, file_names)
    else:
        raise ValueError(f"Unsupported export processing_option: {processing_option}")
