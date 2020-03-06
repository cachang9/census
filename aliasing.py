import pandas as pd


def aliasing(file_name):
    path = "/Users/jiachang/Document/census/final/" + file_name + "_final.csv"
    output_path = "/Users/jiachang/Document/census/alias/" + file_name + ".csv"
    header = []
    for i in range(1, 2248):
        name = "AA" + str(i)
        name_e = "AA" + str(i) + "_E"
        header.append(name)
        header.append(name_e)
    df = pd.read_csv(path)
    df = df.drop(columns=["Unnamed: 0", 'year_E', 'GeoCode_E', 'GeoName_E'])
    header.append("year")
    header.append("GeoCode")
    header.append("GeoName")
    df.columns = header
    # df = df.drop(columns=["unnamed: 0"])
    df.to_csv(output_path)


if __name__ == "__main__":
    aliasing("TERRITORIES")
