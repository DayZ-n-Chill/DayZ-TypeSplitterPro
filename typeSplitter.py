import xml.etree.ElementTree as ET
import os
import xml.dom.minidom

def find_cfgeconomycore_xml():
    # Get the directory where the script is located
    script_dir = os.path.dirname(__file__)
    # Ascend one directory level to the parent directory
    parent_dir = os.path.dirname(script_dir)
    # Define the path to the cfgeconomycore.xml file in the parent directory
    cfgeconomycore_file_path = os.path.join(parent_dir, 'cfgeconomycore.xml')
    return cfgeconomycore_file_path

def add_ce_elements_to_cfgeconomycore(files):
    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    if cfgeconomycore_file_path:
        try:
            tree = ET.parse(cfgeconomycore_file_path)
            root = tree.getroot()

            # Create a new 'ce' element for each file and add it to the root
            for file in files:
                ce_element = ET.Element('ce', folder='types')
                file_element = ET.SubElement(ce_element, 'file', name=file, type='types')
                root.append(ce_element)

            # Write the updated content to cfgeconomycore.xml
            tree.write(cfgeconomycore_file_path, encoding='UTF-8', xml_declaration=True)
            print("Added CE elements to cfgeconomycore.xml")
        except ET.ParseError:
            print("Error: The cfgeconomycore.xml file could not be parsed.")
        except FileNotFoundError:
            print("Error: The cfgeconomycore.xml file was not found.")
        except Exception as e:
            print(f"An unexpected error occurred while adding CE elements: {e}")
    else:
        print("Error: cfgeconomycore.xml file path not found.")

def format_cfgeconomycore():
    cfgeconomycore_file_path = find_cfgeconomycore_xml()
    if cfgeconomycore_file_path:
        try:
            tree = ET.parse(cfgeconomycore_file_path)
            root = tree.getroot()

            # Start building the formatted XML string
            formatted_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<economycore>\n\n'

            # Add formatted <classes> element
            formatted_xml += '\t<classes>\n'
            for child in root.find('classes').iter():
                if child.tag == 'rootclass':
                    formatted_xml += f'\t\t<{child.tag} name="{child.get("name")}"'
                    for key, value in child.items():
                        if key != 'name':
                            formatted_xml += f' {key}="{value}"'
                    formatted_xml += '/>\n'
            formatted_xml += '\t</classes>\n\n'

            # Add formatted <defaults> element
            formatted_xml += '\t<defaults>\n'
            for child in root.find('defaults').iter():
                formatted_xml += f'\t\t<{child.tag} name="{child.get("name")}" value="{child.get("value")}"/>\n'
            formatted_xml += '\t</defaults>\n\n'

            # Add formatted <ce> elements grouped into a single <ce> tag
            ce_files = []
            for ce_element in root.findall('ce'):
                for file_element in ce_element.findall('file'):
                    ce_files.append((file_element.get("name"), file_element.get("type")))

            # Adding the consolidated <ce> element
            if ce_files:
                formatted_xml += '\t<ce folder="types">\n'
                for file_name, file_type in ce_files:
                    formatted_xml += f'\t\t<file name="{file_name}" type="{file_type}" />\n'
                formatted_xml += '\t</ce>\n'

            # Finish building the formatted XML string
            formatted_xml += '</economycore>'

            # Write the formatted XML back to cfgeconomycore.xml
            with open(cfgeconomycore_file_path, 'w') as f:
                f.write(formatted_xml)

            print("Formatted cfgeconomycore.xml")
        except ET.ParseError:
            print("Error: The cfgeconomycore.xml file could not be parsed.")
        except FileNotFoundError:
            print("Error: The cfgeconomycore.xml file was not found.")
        except Exception as e:
            print(f"An unexpected error occurred while formatting cfgeconomycore.xml: {e}")
    else:
        print("Error: cfgeconomycore.xml file path not found.")

def save_category_files(categorized_data, types_dir):
    for category, elements in categorized_data.items():
        category_file_path = os.path.join(types_dir, f"{category}.xml")
        category_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<types>\n    '
        for element in elements:
            category_xml += ET.tostring(element, encoding='unicode')
        category_xml += '</types>'
        with open(category_file_path, 'w') as f:
            f.write(category_xml)

def organize_xml_contents():
    script_dir = os.path.dirname(__file__)
    original_file_path = os.path.join(script_dir, 'types.xml')
    backup_file_path = os.path.join(script_dir, 'types.bk')

    if os.path.exists(original_file_path):
        os.rename(original_file_path, backup_file_path)
    else:
        print("Error: The specified file 'types.xml' was not found.")
        return

    tree = ET.parse(backup_file_path)
    root = tree.getroot()
    types_dir = os.path.join(script_dir, 'types')
    os.makedirs(types_dir, exist_ok=True)

    categorized_data = {}
    for type_element in root.findall('type'):
        category_element = type_element.find('category')
        category = category_element.get('name') if category_element is not None else 'uncategorized'
        name = type_element.get('name')
        if name.startswith('AmmoBox_') or name.startswith('Ammo_'):
            category = 'ammo'
        elif name.startswith('Animal_'):
            category = 'animals'
        elif name.startswith('Offroad') or name.startswith('CivilianSedan') or name.startswith('Hatchback') or name.startswith('Sedan') or name.startswith('Truck_01'):
            category = 'vehicles'
        elif name.startswith('Land_Wreck_') or name.startswith('Land_wreck_') or name.startswith('Wreck_'):
            category = 'wrecks'
        elif name.startswith('Land_Container_') or name.startswith('Land_Train_') or name.startswith('ContaminatedArea_Dynamic'):
            category = 'events'
        elif name.startswith('StaticObj_'):
            category = 'staticObjs'
        elif name.startswith('ZmbM_') or name.startswith('ZmbF_'):
            category = 'zombies'
        elif any(usage.get('name') == 'SeasonalEvent' for usage in type_element.findall('usage')):
            category = 'seasonal'
        elif name.startswith('ChristmasTree') or name.startswith('Bonfire') or name.startswith('EasterEgg'):
            category = 'seasonal'
        elif name.startswith('WaterBottle'):
            category = 'containers'

        if category == 'lootdispatch':
            category = 'vehicleParts'

        if category not in categorized_data:
            categorized_data[category] = []
        categorized_data[category].append(type_element)

        if category == 'vehicleParts':
            file_path = os.path.join(types_dir, 'vehicleParts.xml')
        else:
            file_path = os.path.join(types_dir, f"{category}.xml")

    save_category_files(categorized_data, types_dir)
    add_ce_elements_to_cfgeconomycore([f"{category}.xml" for category in categorized_data])
    format_cfgeconomycore()

# Execution
organize_xml_contents()    
