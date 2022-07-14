import json

def generate():
    data = {
        "static_files":[
            "https://zenodo.org/record/3688691/files/rapid_connect_San_Guad.csv",
            "https://zenodo.org/record/3688691/files/k_San_Guad_2004_1.csv",
            "https://zenodo.org/record/3688691/files/x_San_Guad_2004_1.csv",
            "https://zenodo.org/record/3688691/files/riv_bas_id_San_Guad_hydroseq.csv"
        ],
        "dynamic_files":[
            "https://zenodo.org/record/3688691/files/m3_riv_San_Guad_20100101_20131231_VIC0125_3H_utc_err_R286_D.nc"
        ],
        "name_list":"https://raw.githubusercontent.com/c-h-david/rapid/master/tst/rapid_namelist_San_Guad_JHM2",
        "request_name": "San_Guad_JHM2"
    }
    print(json.dumps(data))

if __name__ == "__main__":
    generate()
