echo "STATIC BUILD START"

set -e

# activate the virtual environment
# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv
source venv/bin/activate
# Download and extract wkhtmltox
# yum install compat-openssl10-1.0.2o-4.el8_6.x86_64.rpm --allowerasing -y
# curl -L -o wkhtmltox.zip https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-4/wkhtmltox-0.12.6-4.amazonlinux2_lambda.zip
# unzip wkhtmltox.zip -d /usr/local
# unzip wkhtmltox.zip -d /vercel/path1/venv
# rm wkhtmltox.zip
# # yum install wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm -y
# # yum install libpng-1.5.13-8.amzn2.x86_64.rpm --allowerasing -y
# # yum install fontconfig-2.13.94-2.amzn2023.0.2.x86_64.rpm --allowerasing -y
# # export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/var/task/staticfiles_build/wkhtmltox/lib:$LD_LIBRARY_PATH
# # ln -s /var/task/wkhtmltopdf /usr/local/bin/wkhtmltopdf
# # ln -s /usr/local/lib/libpng15.so.15 /usr/lib64/libpng15.so.15
# # ln -s /usr/lib/libpng15.so.15 /usr/lib64/libpng15.so.15
# # ln -s /usr/lib64/libfontconfig.so.1 /usr/lib64/libfontconfig.so.1
# # ln -s /usr/lib/libfontconfig.so.1 /usr/lib64/libfontconfig.so.1
# ldconfig
# ldd /usr/local/bin/wkhtmltopdf
# ldd wkhtmltopdf

# # Add /usr/local/bin to PATH
# # export PATH=$PATH:/usr/local/bin
# echo "export PATH=\$PATH:/usr/local/bin" >> ~/.bashrc
# echo "export PYTHONPATH=\$PYTHONPATH:/var/task/staticfiles_build/wkhtmltox/bin" >> ~/.bashrc
# source ~/.bashrc

# /vercel/path1/venv/bin/wkhtmltopdf --version
# wkhtmltopdf --version
# which wkhtmltopdf
# which requirements.txt
# chmod +x /usr/local/bin/wkhtmltopdf

# # yum install libpng15 -y
# # rpm -ql /usr/local/wkhtmltox/bin/wkhtmltopdf
# /usr/local/bin/wkhtmltopdf --version

# install all deps in the venv
pip install -r requirements.txt

# collect static files using the Python interpreter from venv
python manage.py collectstatic --noinput

echo "STATIC BUILD END"

# [optional] Start the application here 
# python manage.py runserver
