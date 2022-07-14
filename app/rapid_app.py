from flask import Flask, jsonify, request
import os
import requests
import shutil
import subprocess
import boto3

app = Flask(__name__)

#env
tst_dir = "/"
input_dir = "../input"
output_dir = "../output"
nl_dir = "namelists"
s3_bucket_name = "rapid-output"

def digest_namelist():
    #todo
    pass

def start():
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    if not os.path.isdir(nl_dir):
        os.mkdir(nl_dir)


@app.route('/', methods=['GET', 'POST'])
def index():

    return 'rapid_app'

@app.route('/submit/', methods=['GET', 'POST'])
def welcome():

    print("request received")

    #os.environ['AWS_PROFILE'] = "default"

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket_name)

    request_data = request.get_json()

    sf = request_data['static_files']
    df = request_data['dynamic_files']
    nl = request_data['name_list']
    req_name = request_data['request_name']

    l_id = os.path.join(input_dir,req_name)
    l_od = os.path.join(output_dir,req_name)

    if not os.path.isdir(l_id):
        os.mkdir(l_id)
    if not os.path.isdir(l_od):
        os.mkdir(l_od)

    for url in sf+df:
        r = requests.get(url, stream=True)
        path_to_save = os.path.join(l_id,url.split('/')[-1])
        if "zenodo" in url:
            print(f"{r.headers['X-RateLimit-Remaining']}/{r.headers['X-RateLimit-Limit']}")

        with open(path_to_save, "wb") as outfile:
            for chunk in r.iter_content(chunk_size=None):  # Let the server decide.
                outfile.write(chunk)

        print(f"retrieved file {url} \n ==== \n ")

    if nl.split('/')[-1] not in os.listdir(nl_dir):
        r = requests.get(nl, stream=True)
        path_to_save = os.path.join(nl_dir,nl.split('/')[-1])
        with open(path_to_save, "wb") as outfile:
            for chunk in r.iter_content(chunk_size=None):  # Let the server decide.
                outfile.write(chunk)
        print(f"retrieved file {nl} \n ==== \n ")

    shutil.copy(os.path.join(nl_dir, nl.split('/')[-1]), "rapid_namelist")



    process = subprocess.Popen(['./rapid'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

    #important- will cause wait until process termination
    stdout, stderr = process.communicate()

    print(stdout)
    print(stderr)

    # TODO digest_namelist()
    o_fname = "Qout_San_Guad_nx_method.nc"

    of = os.path.join(l_od, o_fname)

    print(f"output file generated: {of}")

    bucket.upload_file(of, o_fname)

    #with open(of, "rb") as outf:
    #    o_r = outf.read()
    #    return o_r

    bucket_location = boto3.client('s3').get_bucket_location(Bucket=s3_bucket_name)
    if bucket_location == 'None':
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location['LocationConstraint'],
            s3_bucket_name,
            o_fname
        )
    else:
        object_url = "https://s3.amazonaws.com/{0}/{1}".format(
            s3_bucket_name,
            o_fname
        )
    print(f"output file uploaded: {object_url}")


    #returned = f"\n{req_name} \n\n raw data: {request_data} \n static files: {sf} \n dynamic files: {df} \n namelist: {nl}\n"

    return object_url



if __name__ == '__main__':
    start()

    app.run(host='0.0.0.0', port=5000)
