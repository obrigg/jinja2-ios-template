import jinja2
import os

template_file = "catalyst9300-template.j2"
csv_parameter_file = "sample.csv"
config_parameters = []
output_directory = "_output"

# 1. read the contents from the CSV files
print("Read CSV parameter file...")
f = open(csv_parameter_file)
csv_content = f.read()
f.close()

# 2. for Jinja2, we need to convert the given CSV file into the a python
# dictionary to get the script a bit more reusable, I will not statically
# limit the possible header values (and therefore the variables)
print("Convert CSV file to dictionaries...")
csv_lines = csv_content.splitlines()
headers = csv_lines[0].split(",")
for i in range(1, len(csv_lines)):
    values = csv_lines[i].split(",")
    parameter_dict = dict()
    interfaces = {}
    vlans = []
    for h in range(0, len(headers)):
        parameter_dict[headers[h]] = values[h]
# Create a list of vlans from the input
    vlans = parameter_dict['vlans'].split(";")
    parameter_dict['vlans'] = vlans
# Create a dict of interfaces and their vlans
    for key in parameter_dict:
        if key.startswith('Gi') or key.startswith('Te'):
            interfaces[key] = parameter_dict[key]
    for key in interfaces:
        del parameter_dict[key]
    parameter_dict['interfaces'] = interfaces

    config_parameters.append(parameter_dict)

# 3. next we need to create the central Jinja2 environment and we will load
# the Jinja2 template file
print("Create Jinja2 environment...")
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
template = env.get_template(template_file)

# we will make sure that the output directory exists
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# 4. now create the templates
print("Create templates...")
for parameter in config_parameters:
    result = template.render(parameter)
    f = open(os.path.join(output_directory, parameter['hostname'] + ".cfg"), "w")
    f.write(result)
    f.close()
    print("Configuration '%s' created..." % (parameter['hostname'] + ".cfg"))
print("DONE")
