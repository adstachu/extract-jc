import json
import os

def find_objects_by_class(json_data, class_name, parent_key=None, path=[]):
    # recursive search for objects
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == class_name:
                yield (json_data, path)
            elif isinstance(value, (dict, list)):
                yield from find_objects_by_class(value, class_name, key, path + [key])
    elif isinstance(json_data, list):
        for index, item in enumerate(json_data):
            if isinstance(item, (dict, list)):
                yield from find_objects_by_class(item, class_name, parent_key, path + [str(index)])

def save_objects_to_files(objects_with_paths, base_filename):
    # save each object to its own file
    for index, (obj, path) in enumerate(objects_with_paths):
        tenant_name = obj.get('fvTenant', {}).get('attributes', {}).get('name', f"{base_filename}_{index}")
        filename = f"{tenant_name}.json"
        object_data_with_header_footer = {
            "totalCount": "1",
            "imdata": [obj]
        }
        with open(filename, 'w') as outfile:
            json.dump(object_data_with_header_footer, outfile, indent=2)
        print(f"Saved object to {filename}")

def process_json_file(input_json_file, class_name, output_file_prefix):
    # load json data from an input file
    with open(input_json_file, 'r') as infile:
        data = json.load(infile)

    # find objects by paths
    objects_with_paths = list(find_objects_by_class(data, class_name))

    # save each object to its own file
    save_objects_to_files(objects_with_paths, output_file_prefix)

def main(input_folder, class_name, output_file_prefix):
    # iterate over all files in the input folder and process each JSON file.
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            print(f"Processing {filename}...")
            process_json_file(os.path.join(input_folder, filename), class_name, output_file_prefix)

if __name__ == "__main__":
    input_folder_path = 'input'
    class_to_find = 'fvTenant'
    output_prefix = 'output' 

    main(input_folder_path, class_to_find, output_prefix)
