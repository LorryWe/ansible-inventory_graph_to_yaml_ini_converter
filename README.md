# ansible-inventory_graph_to_yaml_ini_converter
Converts ansible-inventory --graph output to yaml or ini format for ansible use

## Usage:
`convert_graph_inventory.py -i <output from ansible-inventory --graph> [-u <unique ref        , e.g. foremanservername>] [-o <outputfile>] [-f <format> default yaml or ini]`

## Introduction:
Use the convert_graph_inventory.py utility script to convert graph output from built in ansible plugin: foreman-inventory (contains list of hostgroups and managed nodes), into a yaml inventory format (soon to be ini format too) which is useable by ansible for 'other stuff'.

The instructions below describe how to use the script, plus provide a simple example of how ansible can then make use of multiple inventories, so that a constant list of variable / values contained in one inventory file, may be combined with the dynamic inventory (created using this utility script) and applied to managed nodes.

## Method Overview:
- Use ansible-inventory utility to create foreman inventory_graph_format file
- Use convert_graph_inventory.py utility script to process inventory_graph_format (created above), to create inventory_hostgroups_and_nodes file for use with ansible
- Update inventory_vars as required to match derived groupnames in inventory_hostgroups_and_nodes file (created above)
- Run ansible playbook

## Create inventory_graph_format file:
Create a inventory_graph_format file by renaming foreman.yaml.template file to your_foreman_foreman.yaml, then edit appropriately to enable access your foreman instance (e.g. using normal or api user).

Next run:

`ansible-inventory -i ./your_foreman_foreman.yaml --graph --output somefile_inventory.txt`

## Create inventory_hostgroups_and_nodes file:
Next, use the convert_graph_inventory.py utility script converter to create an inventory file in yaml or ini format:

`./convert_graph_inventory.py -i somefile_inventory.txt -f foreman_server_name_`

Note - Although optional, setting a foreman_server_name_ ensures you can uniquely refer to hostgroups when using inventory_hostgroups_and_nodes files from mulitple foreman servers... especially where some managed nodes may not be contained within a hostgroup, so appear in 'ungrouped'

## Update inventory_vars file:
Copy and edit supplied inventory_vars files - e.g. set appropriate variable names and values, plus hostgroup names (depending on inventory_hostgroups_and_nodes file)

## Update playbook file to suit:
You can guess the rest! - a basic playbook yaml file has been supplied which includes an example of how to refer to variables held in inventory files. To run the demo playbook, use:

`ansible-playbook -i -i ./inventory_hostgroups_and_nodes -i ./inventory_vars playbooks/multi_inventory_playbook_test.yaml -u root --ask-pass`

