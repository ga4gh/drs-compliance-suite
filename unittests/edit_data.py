import json
import os

def write_drs_object(drs_object):
    obj_id = drs_object["id"]
    data = {}

    # Get the existing data
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'drs_objects.json')

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    data[obj_id] = drs_object

    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return drs_object

def get_all_drs_objects():
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'drs_objects.json')

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    return data

def get_drs_object(drs_id, expand = False):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'drs_objects.json')
    
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        # Check if object exists
        if drs_id in data:  
            if data[drs_id]["is_bundle"] == "1":
                contents = []
                bundle_path = os.path.join(curr_dir, 'data', 'drs_objects_bundles.json')                    
                with open(bundle_path, 'r') as bundle_file:
                    bundles = json.load(bundle_file)
                    if drs_id in bundles:
                        for children in bundles[drs_id]:
                            bundle = get_bundle_object(children, expand)
                            drs_object = {
                                "name": "",
                                "id": "",
                                "drs_uri": "",
                                "contents": ""
                            }
                            drs_object["name"] = bundle["name"]
                            drs_object["id"] = bundle["id"]
                            drs_object["drs_uri"] = "" #bundle[""]
                            if bundle["contents"]:
                                drs_object["contents"] = bundle["contents"]
                            else:
                                drs_object["contents"] = []
                            contents.append(drs_object)
                data[drs_id]["contents"] = contents
                return data[drs_id]
            else:
                return data[drs_id]

def get_bundle_object(drs_id, expand):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'drs_objects.json')
    
    with open(path, 'r') as json_file:
        data = json.load(json_file)        
        # Check if object exists
        if drs_id in data:                      
            if expand == True:            
                bundle_path = os.path.join(curr_dir, 'data', 'drs_objects_bundles.json')
                contents = []
                with open(bundle_path, 'r') as bundle_file:
                    bundles = json.load(bundle_file)
                    if drs_id in bundles:
                        for children in bundles[drs_id]:
                            bundle = get_bundle_object(children, expand)
                            drs_object = {
                                "name": "",
                                "id": "",
                                "drs_uri": "",
                                "contents": ""
                            }
                            drs_object["name"] = bundle["name"]
                            drs_object["id"] = bundle["id"]
                            drs_object["drs_uri"] = "" #bundle[""]
                            if bundle["contents"] and expand == True:
                                drs_object["contents"] = bundle["contents"]
                            else:
                                drs_object["contents"] = []
                            contents.append(drs_object)
                data[drs_id]["contents"] = contents
                return data[drs_id]
            else:
                drs_object = {
                                "name": data[drs_id]["name"],
                                "id": data[drs_id]["id"],
                                "drs_uri": "",
                                "contents": ""
                            }
                return drs_object

def get_drs_object_passport(drs_id):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'drs_object_passport_mapping.json')

    with open(path, 'r') as json_file:
        data = json.load(json_file)

        # Check if object exists
        if drs_id in data:
            return data[drs_id]

def get_drs_access_url(drs_id, access_id):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'drs_object_access_url_mapping.json')

    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        # Check if object exists AND access ID is correct
        if drs_id in data and data[drs_id]["accessId"] == access_id:
            return data[drs_id]["url"]