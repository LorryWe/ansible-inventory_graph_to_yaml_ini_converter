# ansible-inventory_graph_to_yaml_ini_converter
Converts ansible-inventory --graph output to yaml or ini format for ansible use

## Introduction:
Use the convert_graph_inventory.py script to convert graph output from built in ansible plugin: foreman-inventory (contains list of hostgroups and managed nodes), into a yaml inventory format (soon to be ini format too) which is useable by ansible for 'other stuff'.

## Usage:
`convert_graph_inventory.py -i <output from ansible-inventory --graph> [-f <foremanservername>] [-o <outputfile>]'`

## Create initial graph inventory file from foreman:
The script requires graph output to pre-exist in a text file. Create graph output inventory file by renaming foreman.yaml.template file to your_foreman_foreman.yaml, then edit appropriately to enable access your foreman instance.

If later on, you intend to use inventories from multiple foreman servers make sure you enter something unique as group_prefix, this will ensure you can still uniquely refer to hostgroups from different foreman servers, even where they have the same local name.

Next run:

`ansible-inventory -i ./your_foreman_foreman.yaml --graph --output somefile_inventory.txt`

## Create ansible inventory file ready to use:
Next, use the converter to create a yaml (or ini) inventory file:

`./convert_graph_inventory.py -i somefile_inventory.txt -f foremantest`

## Edit inventory vars file to suite:
Copy and edit supplied inventory_vars files - e.g. set appropriate variable names and values, plus hostgroup names (depending on inventory_hostgroups_and_nodes file)

## Copy and edit playbook file to suite:
You can guess the rest! - a basic playbook has been supplied which includes an example of how to refer to variables held in inventory files. To run the demo playbook, use:

`ansible-playbook -i -i ./inventory_hostgroups_and_nodes -i ./inventory_vars playbooks/multi_inventory_playbook_test.yaml -u root --ask-pass`

