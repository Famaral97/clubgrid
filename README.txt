## Accessing database locally
1. mysql -u flaskuser -p
2. Enter password: [ENTER_PASSWORD]
3. use flaskdb
4. show tables;

## Making changes to the database
1. Change the Models as desired (e.g. add new property/column to Clubs)
2. Run `alembic revision --autogenerate -m "<Commit Message>"`
3. This will create a new file in `.migrations/versions/` with the desired change
4. Make sure the db is ready for connections (just wait a couple of seconds)
5. Build the flask app `docker-compose up -d --build flask`
6. This should run the alembic upgrades and update the database

Notes:
1. not tested yet for deployment, but in theory we should just need to run `alembic upgrade head` before running flask.
2. maybe there is a clever way to deal with the env vars. Problem is that we run `alembic revision` in the CLI.

## Merging with transfermarket
1. Add crawler's `club.csv to `/transfermarket` folder
2. Export own .csv from the excel to same folder
3. run `load_dataset.py`, which will create the `/data/data.csv`