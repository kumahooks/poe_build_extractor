import logging
from build_loader import load_build_codes
from build_importer import import_code_handle
from build_parser import parse_build_xml
from file_utils import save_build_to_file

def main():
	logging.basicConfig(level=logging.INFO, format='(%(asctime)s - %(levelname)s): %(message)s')

	try:
		build_codes = load_build_codes('build_codes.json')
	except Exception as e:
		logging.error(f"Failed to load build codes: {e}")
		return

	for build in build_codes:
		logging.info(f"Processing build: {build['name']}")
		xml_data = import_code_handle(build['code'])

		if xml_data:
			try:
				build_data = parse_build_xml(xml_data)
				save_build_to_file(build['name'], build_data)
			except Exception as e:
				logging.error(f"Failed to process build '{build['name']}': {e}")
		else:
			logging.error(f"Failed to import code for build: {build['name']}")

if __name__ == "__main__":
	main()
