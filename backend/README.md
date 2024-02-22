## Instructions for getting the backend up
1) install mongo server and run the command `sudo systemctl start mongod` and check status with `sudo systemctl status mongod`
2) install the requirements: `pip install -r requirements.txt`
2) issue the command `python run.py` inside the `backend directory`

### IF YOU MAKE A CHANGE TO THE DATABASE SCHEMA
in `__init__.py`, add the line `db.["users"].drop()` (replace users with the name of the table) and after you save it will recompile, dropping the table. then  you can remove this line and the table will be recreated with the new schema