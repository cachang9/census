import qc
import error
import aliasing

list_of_region = ["ATLANTIC", "BRITISH_COLUMBIA", "ONTARIO", "PRAIRIES", "QUEBEC", "TERRITORIES"]
list_of_genders = ["Male", "Female", "Total - Sex"]
list_of_gender = ["Male", "Female"]

for region in list_of_region:
    for gender in list_of_gender:
        print("begin processing " + region + " " + gender)
        qc.transform_validate(region, gender)
        error.adding_error_col(region, gender)
        # aliasing.aliasing(region)


print("finish process")
