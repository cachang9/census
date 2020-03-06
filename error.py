import pandas as pd
import math


def adding_error_col(province):
    check_file = "./transformed/" + province + ".csv"
    final_path = "./final/"
    code = ["...", "..", "F", "x"]
    df = pd.read_csv(check_file)
    df = df.drop(columns=['Unnamed: 0'])
    i = 0
    for key, value in df.iteritems():
        print("adding error column for " + key)
        err = value.copy()
        for j in range(len(err)):
            if err[j] not in code:
                err.loc[j] = math.nan
            if value[j] in code:
                value.loc[j] = math.nan
        df.insert(i + 1, df.columns[i] + "_E", err)
        i = i + 2
    print("Write final output file")
    df.to_csv(final_path + province + "_final.csv")


if __name__ == "__main__":
    print("testing")
    adding_error_col("TERRITORIES")
