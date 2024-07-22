import xml.etree.ElementTree as ET
import logging
from typing import Dict, List, Optional, Union

logging.basicConfig(level=logging.INFO, format='(%(asctime)s - %(levelname)s): %(message)s')

def parse_build_xml(xml_data: str) -> Dict[str, Union[Dict[str, str], List[Dict[str, Optional[str]]]]]:
	logging.info("Starting to parse XML data...")

	try:
		root = ET.fromstring(xml_data)
	except ET.ParseError as e:
		logging.error(f"Failed to parse XML data: {e}")
		return {}

	build = root.find('Build')
	if build is None:
		logging.error("Build element not found in XML.")
		return {}

	build_info = {
		'build_info': extract_build_info(build),
		'stats': extract_stats(build),
		'gems': extract_gems(root),
		'items': extract_items(root)
	}

	logging.info("Finished parsing XML data.")
	return build_info

def extract_build_info(build: ET.Element) -> Dict[str, Optional[str]]:
	logging.info("Extracting build info...")

	return {
		'level': build.get('level'),
		'targetVersion': build.get('targetVersion'),
		'pantheonMajorGod': build.get('pantheonMajorGod'),
		'pantheonMinorGod': build.get('pantheonMinorGod'),
		'bandit': build.get('bandit'),
		'className': build.get('className'),
		'ascendClassName': build.get('ascendClassName'),
		'characterLevelAutoMode': build.get('characterLevelAutoMode'),
		'mainSocketGroup': build.get('mainSocketGroup'),
		'viewMode': build.get('viewMode')
	}

def extract_stats(build: ET.Element) -> Dict[str, str]:
	logging.info("Extracting player stats.")

	stats = {}
	for player_stat in build.findall('PlayerStat'):
		stat_name = player_stat.get('stat')
		stat_value = player_stat.get('value')
		if stat_name and stat_value:
			stats[stat_name] = stat_value

	logging.debug(f"Extracted stats: {stats}")
	return stats

def extract_gems(root: ET.Element) -> Dict[str, List[Dict[str, Optional[str]]]]:
	logging.info("Extracting gems...")

	gems_info = {}
	skills = root.find('Skills')
	if skills is not None:
		for skill_set in skills.findall('SkillSet'):
			for skill in skill_set.findall('Skill'):
				slot = skill.get('slot') or 'notRecognizedSlot'

				if slot not in gems_info:
					gems_info[slot] = []

				for gem in skill.findall('Gem'):
					gem_info = {
						'name': gem.get('nameSpec'),
						'level': gem.get('level'),
						'gem_id': gem.get('gemId'),
						'variant_id': gem.get('variantId'),
						'skill_id': gem.get('skillId'),
						'quality': gem.get('quality'),
						'quality_id': gem.get('qualityId'),
						'enabled': gem.get('enabled') == 'true'
					}

					gems_info[slot].append(gem_info)

	logging.debug(f"Extracted gems: {gems_info}")
	return gems_info

def extract_items(root: ET.Element) -> List[Dict[str, Optional[str]]]:
	logging.info("Extracting items.")
	items_info = []
	items = root.find('Items')
	if items is not None:
		for item in items.findall('Item'):
			item_info = {
				'id': item.get('id'),
				'rarity': None,
				'name': None,
				'base': None,
				'properties': []
			}

			item_lines = item.text.strip().split('\n')
			if len(item_lines) >= 3:
				item_info['rarity'] = item_lines[0].split(': ')[1].strip()
				item_info['name'] = item_lines[1].strip()
				item_info['base'] = item_lines[2].strip()

				item_info['properties'] = [line.strip() for line in item_lines[3:]]
			else:
				logging.warning(f"Item with id {item.get('id')} has fewer than 3 lines.")

			items_info.append(item_info)

	logging.debug(f"Extracted items: {items_info}")
	return items_info
