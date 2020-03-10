import pandas as pd
import math

# this function add error columns to each column of the transformed file
def adding_error_col(province, gender):
    check_file = "./transformed/" + province + "_" + gender + ".csv"
    final_path = "./final/"
    code = ["...", "..", "F", "x"]
    df = pd.read_csv(check_file)
    df = df.drop(columns=['Unnamed: 0'])
    i = 0
    for key, value in df.iteritems():
        print("adding error column for " + key)
        err = value.copy()
        for j in range(len(err)):
            # move error code into error column
            if err[j] not in code:
                err.loc[j] = math.nan
            # remove error code from original column
            if value[j] in code:
                value.loc[j] = math.nan
        df.insert(i + 1, df.columns[i] + "_E", err)
        i = i + 2
    print("Write final output file")
    df.to_csv(final_path + province + "_" + gender + "_final.csv")


if __name__ == "__main__":
    print("testing")
    adding_error_col("TERRITORIES", "Male")
