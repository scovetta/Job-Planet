#!/bin/bash

# create_environment.sh
# Requirements
REQUIRED=(virtualenv git pip wget)
for required in ${REQUIRED[@]}; do
    hash ${required} 2>&- || { echo >&2 "${required} must be installed first. Aborting."; exit 1; }
done

# Create basic environment
ROOT=${1:-.}
cd $ROOT
ROOT=`pwd`
echo "Using root path: $ROOT"

cd $ROOT
echo "Creating project and app directories"
mkdir -p project app

echo "Creating virtualenv"
cd project
virtualenv --no-site-packages --distribute .

echo "Activating virtualenv"
source ./bin/activate

echo "Path is now $PATH"

echo "Cloning source code repository"
cd ../app
git clone "https://scovetta@github.com/cbsamp/Grand-Central.git" .

echo "Installing buildout"
cd ../project
wget "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"
echo -e "[buildout]\nparts = \n" > ./buildout.cfg
python bootstrap.py

echo "Installing depdendencies"
cd ../app
pip install -r ./settings/virtualenv/REQUIREMENTS

echo "Creating ancillary directories"
cd ../project
mkdir -p cache db log pid sock tmp uploads static

export PYTHONPATH=$ROOT/app:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=settings.settings

echo "Creating gcactivate and gcstart scripts"
echo "#!/bin/bash" > $ROOT/gcactivate.sh
echo "export PYTHONPATH=$ROOT/app/" >> $ROOT/gcactivate.sh
echo "export DJANGO_SETTINGS_MODULE=settings.settings" >> $ROOT/gcactivate.sh
echo "source $ROOT/project/bin/activate" >> $ROOT/gcactivate.sh

echo "#!/bin/bash" > $ROOT/gcstart.sh
echo "ROOT=$ROOT" >> $ROOT/gcstart.sh
echo "source $ROOT/project/bin/activate" >> $ROOT/gcstart.sh
echo "export PYTHONPATH=$PYTHONPATH" >> $ROOT/gcstart.sh
echo "export DJANGO_SETTINGS_MODULE=settings.settings" >> $ROOT/gcstart.sh
echo "python $ROOT/project/bin/django-admin.py run_gunicorn" >> $ROOT/gcstart.sh
echo "deactivate" >> $ROOT/gcstart.sh

echo "Creating database"
cd ../app
django-admin.py validate
django-admin.py syncdb --noinput
django-admin.py migrate
django-admin.py loaddata settings/initial_data/initial_data.json