import pandas as pd
import numpy as np
# Since the headers are missing in the csv file, explicitly passing the field names in the program
csv_file = pd.DataFrame(pd.read_csv("datas/EURJPY_D1.csv", sep=",",
                        names=["time", "open", "high", "low", "close", "volume"], index_col=False))
csv_file.to_json("static/json/EURJPY_D1.json", orient="records", date_format="epoch",
                 double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)
