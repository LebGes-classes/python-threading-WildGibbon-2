import time

import data_analytics.analizes_instruments as inst
import pandas as pd
import os


def main():
    start = time.time()
    data_frames = []

    for file_name in os.listdir("data"):
        if file_name.endswith(".xlsx"):
            data_frames.append(pd.read_excel("data/" + file_name))

    for i, df in enumerate(data_frames):
        with pd.ExcelWriter(f"output/output_{i}.xlsx") as writer:
            inst.sort_by_calibration_dates(df).to_excel(writer, sheet_name="Sheet1")
            inst.filter_warranty(df).to_excel(writer, sheet_name="Sheet2")
            inst.sort_by_issues(df).to_excel(writer, sheet_name="Sheet3")

    print(f"Finished in {time.time() - start} seconds")


if __name__ == "__main__":
    main()
