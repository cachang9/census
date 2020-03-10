import pandas as pd
import numpy as np
import math


# this function is to create a transformed census files, and validate it with the original file
def transform_validate(province, gender):
    check_file = "./98-401-X2016044_" + province + "_eng_CSV/98-401-X2016044_" + province + "_English_CSV_data.csv"
    trans_file_path = "./transformed/"
    check = pd.read_csv(check_file)
    dim_int = 0
    # drop unnecessary gender dimensions
    if gender == "Total - Sex":
        check = check.drop(columns=['Dim: Sex (3): Member ID: [2]: Male', 'Dim: Sex (3): Member ID: [3]: Female'])
        dim_int = 1
    elif gender == "Male":
        check = check.drop(
            columns=['Dim: Sex (3): Member ID: [1]: Total - Sex', 'Dim: Sex (3): Member ID: [3]: Female'])
        dim_int = 2
    elif gender == "Female":
        check = check.drop(
            columns=['Dim: Sex (3): Member ID: [1]: Total - Sex', 'Dim: Sex (3): Member ID: [2]: Male'])
        dim_int = 3
    else:
        raise
    log = []
    # setting up the number of splits to perform on the original file
    num_arr = int(check.shape[0] / 2247)
    # error codes
    blank_out = ["...", "..", "F", "x"]
    total = []

    print("Begin Transforming")
    # sub_total is array of arrays, they are the files that will be transformed
    sub_total = np.array_split(check["Dim: Sex (3): Member ID: [" + str(dim_int) + "]: " + gender], num_arr)
    # sub_check is the original file (used for comparision later), also array of array
    sub_check = sub_total[:]
    # create header files
    h = check["DIM: Profile of Dissemination Areas (2247)"]
    head = pd.Series(h[0:2247])
    header = head.append(pd.Series(["year", "GeoCode", "GeoName"]))
    # creating the arrays for year, geo_code, geo_name
    sub_year = np.array_split(check["CENSUS_YEAR"], num_arr)
    sub_geo_code = np.array_split(check["GEO_CODE (POR)"], num_arr)
    sub_geo_name = np.array_split(check["GEO_NAME"], num_arr)
    for i in range(len(sub_total)):
        # for each array in sub_total, it will be modify into 1 row of entry for the final dataframe, and append to the final dataframe. (
        # (in essence a transposition of the original census file)
        sub_total[i] = sub_total[i].reset_index(drop=True)
        sub_year[i] = sub_year[i].reset_index(drop=True)
        sub_geo_code[i] = sub_geo_code[i].reset_index(drop=True)
        sub_geo_name[i] = sub_geo_name[i].reset_index(drop=True)
        year = sub_year[i][0]
        geo_code = sub_geo_code[i][0]
        geo_name = sub_geo_name[i][0]
        add_on = pd.Series([year, geo_code, geo_name])
        # temp is constructed with extending the sub_total array
        temp = sub_total[i].append(add_on)
        temp = temp.reset_index(drop=True)
        total.append(temp)

    test = pd.DataFrame.from_records(total)
    test.columns = header

    print("Begin Checking")
    # looping through sub_total and sub_check to check for any differences in value
    for j in range(len(sub_check)):
        sub_check[j] = sub_check[j].reset_index(drop=True)
        for k in range(2247):
            if sub_check[j][k] in blank_out:
                sub_check[j][k] = math.nan
            if sub_total[j][k] in blank_out:
                sub_total[j][k] = math.nan
            if float(sub_total[j][k]) != float(sub_check[j][k]) and (not math.isnan(float(sub_total[j][k])) or not math.isnan(float(sub_check[j][k]))):
                print("Found error" + "   " + str(sub_total[j][k]) + "   " + str(sub_check[j][k]))
                log.append((j, k, sub_total[j][k], sub_check[j][k]))

    if len(log) == 0:
        print("No Error Found")
    else:
        print("Error Found, output log file")
        with open("error_log.txt", "w") as output:
            output.write(str(log))

    print("Write Output File")
    test.to_csv(trans_file_path + province + "_" + gender + ".csv")


if __name__ == "__main__":
    transform_validate("TERRITORIES", "Male")
