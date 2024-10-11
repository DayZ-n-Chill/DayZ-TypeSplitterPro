import xml.etree.ElementTree as ET
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_cfgeconomycore_xml():
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, 'cfgeconomycore.xml')

def add_ce_elements_to_cfgeconomycore(files):
    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    try:
        tree = ET.parse(cfgeconomycore_file_path)
        root = tree.getroot()

        for file in files:
            ce_element = ET.Element('ce', folder='types')
            ET.SubElement(ce_element, 'file', name=file, type='types')
            root.append(ce_element)

        tree.write(cfgeconomycore_file_path, encoding='UTF-8', xml_declaration=True)
        logging.info("Added CE elements to cfgeconomycore.xml")
    except (ET.ParseError, FileNotFoundError) as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def format_cfgeconomycore():
    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    try:
        tree = ET.parse(cfgeconomycore_file_path)
        root = tree.getroot()

        formatted_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<economycore>\n\n'
        formatted_xml += '\t<classes>\n'
        for child in root.find('classes').iter('rootclass'):
            formatted_xml += f'\t\t<{child.tag} name="{child.get("name")}"'
            formatted_xml += ''.join([f' {k}="{v}"' for k, v in child.items() if k != 'name'])
            formatted_xml += '/>\n'
        formatted_xml += '\t</classes>\n\n'

        formatted_xml += '\t<defaults>\n'
        for child in root.find('defaults'):
            formatted_xml += f'\t\t<{child.tag} name="{child.get("name")}" value="{child.get("value")}"/>\n'
        formatted_xml += '\t</defaults>\n\n'

        ce_files = [(ce.find('file').get('name'), ce.find('file').get('type')) for ce in root.findall('ce')]
        if ce_files:
            formatted_xml += '\t<ce folder="types">\n'
            formatted_xml += ''.join([f'\t\t<file name="{name}" type="{type}" />\n' for name, type in ce_files])
            formatted_xml += '\t</ce>\n'
        formatted_xml += '</economycore>'

        with open(cfgeconomycore_file_path, 'w') as f:
            f.write(formatted_xml)

        logging.info("Formatted cfgeconomycore.xml")
    except (ET.ParseError, FileNotFoundError) as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def save_category_files(categorized_data, types_dir):
    for category, elements in categorized_data.items():
        category_file_path = os.path.join(types_dir, f"{category}.xml")
        category_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<types>\n'
        category_xml += ''.join([ET.tostring(element, encoding='unicode') for element in elements])
        category_xml += '</types>'
        with open(category_file_path, 'w') as f:
            f.write(category_xml)

def categorize_elements(root):
    categories = {
        'ammo': lambda name: name.startswith(('AmmoBox_', 'Ammo_')),
        'animals': lambda name: name.startswith('Animal_'),
        'vehicles': lambda name: name.startswith(('Offroad', 'CivilianSedan', 'Hatchback', 'Sedan', 'Truck_01')),
        'wrecks': lambda name: name.startswith(('Land_Wreck_', 'Land_wreck_', 'Wreck_')),
        'events': lambda name: name.startswith(('Land_Container_', 'Land_Train_', 'ContaminatedArea_Dynamic')),
        'staticObjs': lambda name: name.startswith('StaticObj_'),
        'zombies': lambda name: name.startswith(('ZmbM_', 'ZmbF_')),
        'seasonal': lambda name: any(usage.get('name') == 'SeasonalEvent' for usage in type_element.findall('usage')) or name.startswith(('ChristmasTree', 'Bonfire', 'EasterEgg')),
        'containers': lambda name: name.startswith('WaterBottle'),
        'vehicleParts': lambda name: name.startswith('lootdispatch'),
        'uncategorized': lambda name: True
    }

    categorized_data = {key: [] for key in categories}

    for type_element in root.findall('type'):
        name = type_element.get('name')
        for category, condition in categories.items():
            if condition(name):
                categorized_data[category].append(type_element)
                break

    return categorized_data

def organize_xml_contents():
    script_dir = os.path.dirname(__file__)
    original_file_path = os.path.join(script_dir, 'types.xml')
    backup_file_path = os.path.join(script_dir, 'types.bk')

    if os.path.exists(original_file_path):
        os.rename(original_file_path, backup_file_path)
    else:
        logging.error("The specified file 'types.xml' was not found.")
        return

    tree = ET.parse(backup_file_path)
    root = tree.getroot()
    types_dir = os.path.join(script_dir, 'types')
    os.makedirs(types_dir, exist_ok=True)

    categorized_data = categorize_elements(root)
    save_category_files(categorized_data, types_dir)

    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    add_ce_elements_to_cfgeconomycore([f"{category}.xml" for category in categorized_data if categorized_data[category]])
    format_cfgeconomycore()

# Execution
organize_xml_contents()
