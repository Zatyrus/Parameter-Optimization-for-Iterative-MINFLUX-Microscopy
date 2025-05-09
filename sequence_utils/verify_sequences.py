## dependencies
from sequence_tools import MFXSequenceTools
import argparse
import os

# add parser for command line arguments
parser = argparse.ArgumentParser(description="Verify MFX sequence files.")
parser.add_argument(
    "-d", "--dir", type=str, required=True, help="Root directory containing json files."
)


def run_verification(root: str, filetype: str = ".json") -> None:
    """
    Function to run the verification on the json files.
    """
    # Initialize the MFXSequenceTools class
    mfx_sequence_tools = MFXSequenceTools(root, filetype)

    # Run the verification
    verification_results = mfx_sequence_tools.verify()

    # Print the results
    print("Verification Results:")
    for key, value in verification_results.items():
        print(f"{key}: {value}")

    return print("\nVerification complete.")


if __name__ == "__main__":
    # Parse the command line arguments
    root = parser.parse_args().dir
    root = os.path.abspath(root)
    # Check if the directory exists
    if not os.path.exists(root):
        raise FileNotFoundError(f"Directory {root} does not exist.")
    # Check if the directory is a directory
    if not os.path.isdir(root):
        raise NotADirectoryError(f"{root} is not a directory.")
    # Check if the directory is empty
    if not os.listdir(root):
        raise ValueError(f"Directory {root} is empty.")
    # Run the verification
    print(f"Verifying sequence files in: {root}\n")
    run_verification(root)
