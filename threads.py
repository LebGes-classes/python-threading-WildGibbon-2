from concurrent import futures

import data_analytics.analizes_instruments as inst
import pandas as pd
import time
import os

def write_excel_multi_df(sheets: list[pd.DataFrame], path) -> None:
    with pd.ExcelWriter(path) as writer:
        for i, sheet in enumerate(sheets):
            sheet.to_excel(writer, sheet_name=f'Sheet{i}')


if __name__ == '__main__':
    start = time.time()

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        files = ["data/" + file_name for file_name in os.listdir("data") if file_name.endswith(".xlsx")]
        data_frames = list(executor.map(pd.read_excel, files))

        filtered_warranty = list(executor.map(inst.filter_warranty, data_frames))
        sorted_by_issues = list(executor.map(inst.sort_by_issues, data_frames))
        sorted_by_calibration = list(executor.map(inst.sort_by_calibration_dates, data_frames))

        futures_df = []

        for i in range(len(data_frames)):
            sheets = [filtered_warranty[i], sorted_by_issues[i], sorted_by_calibration[i]]
            futures_df.append(executor.submit(write_excel_multi_df, sheets, path="output/output_" + str(i) + ".xlsx"))

    print(time.time() - start)