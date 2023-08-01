# build_files.sh
echo "==========********============="
pip install -r requirements.txt
python3.9 manage.py collectstatic
echo "==========########============="