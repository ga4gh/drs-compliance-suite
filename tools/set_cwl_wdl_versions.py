import json
import os

curr_dir = os.path.dirname(__file__)

''' GET  VERSION '''
parent_dir = os.path.dirname(curr_dir)

setup_py_path = os.path.join(parent_dir, 'setup.py')
with open(setup_py_path,'r') as file:
    setup_py_string = "".join(file.readlines()) # read the setup.py file into a string
    version = setup_py_string.split('version="')[1].split('",')[0] # grab the version

''' FOR WDL '''
def set_wdl_json():
    wdl_path = os.path.join(curr_dir, 'wdl', 'drs_compliance_suite.wdl.json')

    with open(wdl_path,'r') as jsonfile:
        wdl_json = json.load(jsonfile)

    wdl_json["drsComplianceReportWorkflow.version"] = version

    with open(wdl_path, 'w') as file:
        json.dump(wdl_json, file, indent=4)

''' FOR CWL (Not used because couldn't figure out how to use $(inputs.version) in .cwl.json) '''
def set_cwl_json():
    cwl_path = os.path.join(curr_dir, 'cwl', 'drs_compliance_suite.cwl.json')

    with open(cwl_path,'r') as jsonfile:
        cwl_json = json.load(jsonfile)

    cwl_json["version"] = version

    with open(cwl_path, 'w') as file:
        json.dump(cwl_json, file, indent=4)

''' 
FOR CWL
-Goes to the workflow file (.cwl) and edits the line pulling the docker image
-A temporary solution that should be fixed later. Ideally a "version" variable  
 would be set in the .cwl.json file and the .cwl workflow would grab it from there
'''
def set_cwl_workflow():
    cwl_path = os.path.join(curr_dir, 'cwl', 'drs_compliance_suite.cwl')

    with open(cwl_path,'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if "dockerPull: ga4gh/drs-compliance-suite:" in lines[i]: # Find the string pulling the docker image
                # version = "test"
                splt = lines[i].split(":") # separate by : and choose the last item (the version)
                splt[-1] = "{}\n".format(version) # update the version
                lines[i] = ":".join(splt) # join the line back, and save 
            i += 1

    with open(cwl_path, 'w') as file:
        file.write("".join(lines))

set_wdl_json()
set_cwl_workflow()