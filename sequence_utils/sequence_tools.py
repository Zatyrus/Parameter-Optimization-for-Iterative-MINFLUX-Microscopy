## Dependencies
import os
import json
from glob import glob
from typing import List, Dict, Any


## Functions
class MFXSequenceTools:
    def __init__(self, root: str, filetype: str = ".json") -> "MFXSequenceTools":
        self.root = root
        self.filetype = filetype

        return self.__post_init__()

    def __post_init__(self):
        """
        Function to run after the class is initialized.
        """
        # Grab all file paths in the directory
        self.file_paths = self.grab_file_paths(self.root, self.filetype)

        # Load all json files into a dictionary
        self.json_data = self.load_jsons_to_dict(self.file_paths)

    def verify(self) -> Dict[str, Any]:
        """
        Function to verify the json files.
        """
        # Check for duplicates in the dictionary
        name_duplicates = self.check_for_name_duplications(self.json_data)
        sequence_duplicates = self.check_for_sequence_duplications(self.json_data)

        # Verify that the file names and sequence ids are the same
        name_id_mismatch = self.verify_file_name_and_sequence_ids(self.json_data)

        return {
            "name_duplicates": name_duplicates,
            "sequence_duplicates": sequence_duplicates,
            "name_id_mismatch": name_id_mismatch,
        }

    def grab_file_paths(self, root: str, filetype: str = ".json") -> List:
        """
        Function to grab all file paths in a directory.
        """
        return glob(f"{root}/**/*{filetype}", recursive=True)

    def load_json(self, json_path: str) -> Dict[str, Any]:
        """
        Function to load a json file.
        """
        with open(json_path, "r") as f:
            data = json.load(f)
        return data

    def load_jsons_to_dict(self, json_paths: List[str]) -> Dict[str, Any]:
        """
        Function to load multiple json files into a dictionary.
        """
        data = {}
        for json_path in json_paths:
            data[os.path.basename(json_path)] = self.load_json(json_path)
        return data

    def check_for_name_duplications(self, json_data: Dict[str, Any]) -> List[str]:
        """
        Function to check for duplicates in a dictionary.
        """
        seen = set()
        duplicates = []
        for key, value in json_data.items():
            if key in seen:
                duplicates.append(key)
            else:
                seen.add(key)
        return duplicates

    def flatten_dict(
        self, d: Dict[str, Any], parent_key: str = "", sep: str = "_"
    ) -> Dict[str, Any]:
        """
        Function to flatten a nested dictionary.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def hash_dict(self, d: Dict[str, Any]) -> str:
        """
        Function to hash a dictionary.
        """
        import hashlib

        # Convert the dictionary to a string and encode it
        dict_str = json.dumps(d, sort_keys=True).encode()
        # Create a hash object and return the hex digest
        return hashlib.sha256(dict_str).hexdigest()

    def check_for_sequence_duplications(self, json_data: Dict[str, Any]) -> List[str]:
        """
        Function to check for duplicates in a dictionary.
        """
        seen = set()
        duplicates = []
        for key, value in json_data.items():
            if self.hash_dict(value) in seen:
                duplicates.append(key)
            else:
                seen.add(self.hash_dict(value))
        return duplicates

    def verify_file_name_and_sequence_ids(self, json_data: Dict[str, Any]) -> List[str]:
        """
        Function to verify that the file names and sequence ids are the same.
        """
        name_id_mismatches = []
        for key, value in json_data.items():
            if key.split(".")[0] != value["id"]:
                name_id_mismatches.append(
                    f"File name {key} does not match sequence id {value['id']}"
                )
        return name_id_mismatches
