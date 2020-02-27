import qc
import error

list_of_region = ["ATLANTIC", "BRITISH_COLUMBIA", "ONTARIO", "PRAIRIES", "QUEBEC", "TERRITORIES"]


for region in list_of_region:
    print("begin process " + region)
    qc.transform_validate(region)
    error.adding_error_col(region)

print("finish process")