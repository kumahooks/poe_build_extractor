import logging
import json
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='(%(asctime)s - %(levelname)s): %(message)s')

def load_build_codes(filename: str) -> List[Dict[str, Any]]:
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
			return data.get('build_codes', [])
	except FileNotFoundError:
		logging.error(f"File not found: {filename}")
		return []
	except json.JSONDecodeError as e:
		logging.error(f"Failed to decode JSON from file {filename}: {e}")
		return []
