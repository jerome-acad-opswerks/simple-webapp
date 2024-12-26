Activate the environment
. .venv/bin/activate

Install Requirements
pip install -r requirements.txt

Deactivate the environment
deactivate

Run Server
gunicorn -w 4 'app:app'
