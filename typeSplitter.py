import xml.etree.ElementTree as ET
import os
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Debug mode flag
DEBUG_MODE = True  # Set to True for debug mode, False for normal mode

def find_cfgeconomycore_xml():
    # Determine the path to 'cfgeconomycore.xml', which is assumed to be in the parent directory of the script
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, 'cfgeconomycore.xml')

def add_ce_elements_to_cfgeconomycore(files):
    # Add 'ce' elements to the 'cfgeconomycore.xml' file for the given list of files
    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    try:
        # Parse the existing XML file
        tree = ET.parse(cfgeconomycore_file_path)
        root = tree.getroot()

        # Add each file as a new 'ce' element
        for file in files:
            ce_element = ET.Element('ce', folder='types')
            ET.SubElement(ce_element, 'file', name=file, type='types')
            root.append(ce_element)

        # Write changes back to the XML file
        tree.write(cfgeconomycore_file_path, encoding='UTF-8', xml_declaration=True)
        logging.info("Added CE elements to cfgeconomycore.xml")
    except (ET.ParseError, FileNotFoundError) as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def format_cfgeconomycore():
    # Format the 'cfgeconomycore.xml' file to ensure it follows a consistent structure
    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    try:
        # Parse the existing XML file
        tree = ET.parse(cfgeconomycore_file_path)
        root = tree.getroot()

        # Start building the formatted XML content
        formatted_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<economycore>\n\n'
        formatted_xml += '\t<classes>\n'
        for child in root.find('classes').iter('rootclass'):
            formatted_xml += f'\t\t<{child.tag} name="{child.get("name")}"'
            formatted_xml += ''.join([f' {k}="{v}"' for k, v in child.items() if k != 'name'])
            formatted_xml += '/>\n'
        formatted_xml += '\t</classes>\n\n'

        # Add 'defaults' section to the formatted XML
        formatted_xml += '\t<defaults>\n'
        for child in root.find('defaults'):
            formatted_xml += f'\t\t<{child.tag} name="{child.get("name")}" value="{child.get("value")}"/>\n'
        formatted_xml += '\t</defaults>\n\n'

        # Add 'ce' elements for each categorized file
        ce_files = [(ce.find('file').get('name'), ce.find('file').get('type')) for ce in root.findall('ce')]
        if ce_files:
            formatted_xml += '\t<ce folder="types">\n'
            formatted_xml += ''.join([f'\t\t<file name="{name}" type="{type}" />\n' for name, type in ce_files])
            formatted_xml += '\t</ce>\n'
        formatted_xml += '</economycore>'

        # Write the formatted content back to the file
        with open(cfgeconomycore_file_path, 'w') as f:
            f.write(formatted_xml)

        logging.info("Formatted cfgeconomycore.xml")
    except (ET.ParseError, FileNotFoundError) as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def save_category_files(categorized_data, types_dir):
    # Save each category of elements to its own XML file in the specified directory
    for category, elements in categorized_data.items():
        category_file_path = os.path.join(types_dir, f"{category}.xml")
        category_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<types>\n'
        category_xml += ''.join([ET.tostring(element, encoding='unicode') for element in elements])
        category_xml += '</types>\n'
        with open(category_file_path, 'w') as f:
            f.write(category_xml)

def categorize_elements(root):
    # Categorize elements in the XML based on their names or attributes
    categories = {
        # organized by name to make better categorization
        'ammo':          lambda name: name.startswith('Ammo_'),
        'armbands':      lambda name: name.startswith('Armband_'),
        'ammo_boxes':    lambda name: name.startswith('AmmoBox_'),
        'animals':       lambda name: name.startswith('Animal_'),
        'contamination': lambda name: name.startswith(('Land_Container_', 'Land_Train_', 'ContaminatedArea_Dynamic')),
        'flags':         lambda name: name.startswith('Flag_'),
        'staticObjs':    lambda name: name.startswith('StaticObj_'),
        'vehicles':      lambda name: name.startswith(('Offroad', 'CivilianSedan', 'Hatchback', 'Sedan', 'Truck_01', 'Boat_')),
        'wrecks':        lambda name: name.startswith(('Land_Wreck_', 'Land_wreck_', 'Wreck_')),
        'zombies':       lambda name: name.startswith(('ZmbM_', 'ZmbF_', 'Zmbm_')),
        # Seasonal
        'seasonal':      lambda name: any(usage.get('name') == 'SeasonalEvent' for usage in type_element.findall('usage')) or name.startswith(('ChristmasTree', 'Bonfire', 'EasterEgg', 'Aniversary')),
        # Organized by category the way bohemia intended it.
        'clothes':       lambda type_element: type_element.find('category') is not None and type_element.find('category').get('name', '').lower() == 'clothes',
        'containers':    lambda type_element: type_element.find('category') is not None and type_element.find('category').get('name', '').lower() == 'containers',
        'food':          lambda type_element: type_element.find('category') is not None and type_element.find('category').get('name', '').lower() == 'food',
        'tools':         lambda type_element: type_element.find('category') is not None and type_element.find('category').get('name', '').lower() == 'tools',
        'weapons':       lambda type_element: type_element.find('category') is not None and type_element.find('category').get('name', '').lower() == 'weapons',
        'vehicleParts':  lambda type_element: type_element.find('category') is not None and type_element.find('category').get('name', '').lower() == 'lootdispatch',
        'uncategorized': lambda name: True  # Anything that doesn't match the above categories
    }

    categorized_data = {key: [] for key in categories}

    # Iterate over all 'type' elements and categorize them
    for type_element in root.findall('type'):
        name = type_element.get('name')
        for category, condition in categories.items():
            # Use element itself for 'containers', 'vehicleParts', 'weapons', and 'tools' to allow category-based assignment
            if category in ['containers', 'vehicleParts', 'weapons', 'tools', 'food', 'clothes'] and condition(type_element):
                categorized_data[category].append(type_element)
                logging.info(f"Categorized element '{name}' as '{category}'")
                break
            elif category not in ['containers', 'vehicleParts', 'weapons', 'tools', 'food', 'clothes'] and condition(name):
                categorized_data[category].append(type_element)
                logging.info(f"Categorized element '{name}' as '{category}'")
                break

    return categorized_data

def organize_xml_contents():
    # Main function to organize the XML content
    script_dir = os.path.dirname(__file__)
    original_file_path = os.path.join(script_dir, 'types.xml')
    backup_file_path = os.path.join(script_dir, 'types.bk')
    types_dir = os.path.join(script_dir, 'types')

    if DEBUG_MODE:
        # In debug mode, delete the 'types' directory if it exists to start fresh
        if os.path.exists(types_dir):
            shutil.rmtree(types_dir)
            logging.info("Debug mode: Deleted existing 'types' directory")
    else:
        # In normal mode, rename 'types.xml' to 'types.bk' as a backup
        if os.path.exists(original_file_path):
            os.rename(original_file_path, backup_file_path)
        else:
            logging.error("The specified file 'types.xml' was not found.")
            return

    # Parse the XML file (use 'types.xml' in debug mode, 'types.bk' in normal mode)
    tree = ET.parse(original_file_path if DEBUG_MODE else backup_file_path)
    root = tree.getroot()
    os.makedirs(types_dir, exist_ok=True)

    # Categorize the elements in the XML and save them to separate files
    categorized_data = categorize_elements(root)
    save_category_files(categorized_data, types_dir)

    # Add the categorized files to 'cfgeconomycore.xml' and format it
    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    add_ce_elements_to_cfgeconomycore([f"{category}.xml" for category in categorized_data if categorized_data[category]])
    format_cfgeconomycore()

# Execution
organize_xml_contents()
