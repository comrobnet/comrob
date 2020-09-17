# The virtual environment for the comrob project is created using this script.
# Requires virtualenv: $ sudo apt get virtualenv
# to install venv in current directory: $ bash venv.sh venv

# exit on error
set -e

echo "Started creating virtual environment."
# read path from console input
path=$1
# create and source virtual environment
virtualenv -p python3 ${path}
source venv/bin/activate
# install requirements
pip install -r requirements.txt

echo "Finished creating virtual environment."
