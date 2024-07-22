import logging
import base64
import zlib
from typing import Optional

logging.basicConfig(level=logging.INFO, format='(%(asctime)s - %(levelname)s): %(message)s')

def import_code_handle(buf: Optional[str]) -> Optional[str]:
	if not buf:
		return None

	try:
		decoded_data = base64.urlsafe_b64decode(buf)
		xml_text = zlib.decompress(decoded_data)
		return xml_text.decode('utf-8')
	except (base64.binascii.Error, zlib.error, UnicodeDecodeError) as e:
		logging.error(f"Failed to decode or decompress build code: {e}")
		return None
