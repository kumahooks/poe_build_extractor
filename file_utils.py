import logging
import json
import pathlib
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='(%(asctime)s - %(levelname)s): %(message)s')

def save_build_to_file(build_name: str, build_data: dict, directory: str = "loaded_builds") -> None:
	directory_path = pathlib.Path(directory)
	directory_path.mkdir(parents=True, exist_ok=True)
	
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	file_name = f"{build_name}_{timestamp}.json"
	file_path = directory_path / file_name
	
	try:
		with file_path.open('w') as file:
			json.dump(build_data, file, indent=4)
		logging.info(f"Saved build '{build_name}' to {file_path}")
	except Exception as e:
		logging.error(f"Failed to save build '{build_name}': {e}")
