requirements:
- install the requirements with this beautiful bash loop:
`while read requirement; do conda install --yes $requirement; done < requirements.txt`
- install grammar_check with pip: `pip install grammar_check`

preparation
- copy the 'local_settings_template.py' and rename the copy 'local_settings.py'
- never run with public server with DEBUG on!

run server with server.py

flask server runs on port 8090
so it's reachable over the www on: http://lyrik.ddns.net:8090/
