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

## Deploying to Pythonanywhere
1. Update `data.csv` in files root (outside clubgrid folder)
2. Open Bash console
3. `workon myvirtualenv`
4. `./update.sh`
5. `exit`
6. Go upper right corner menu > Web and Reload the web app (big green button)

Notes:
1. not tested yet for deployment, but in theory we should just need to run `alembic upgrade head` before running flask.
2. maybe there is a clever way to deal with the env vars. Problem is that we run `alembic revision` in the CLI.

## Getting and merging transfermarket data
1. Export the manually created excel data to `./transfermarket` as `ClubGrid Logo Labelling - ALL_DATA.csv`
2. In the code comment which countries you want to run the scrapper with
3. Run the `scrapper.py`
4. If the scrapping failed, failed `tfmk_id` and `name` will be output into a `failed_clubs.csv`
5. Repeat from step 2, including the `failed_clubs.csv` ans changing the output file name accordingly until all clubs are scraped
6. Manually merge all of the scraped data into a single .csv
7. Run the `merge_data` function, concatenating all the .csv from transfermarkt scraped data
8. This will merge with the manual labels, creating the final data file `./data/data.csv`

## Validating Conditions
1. Run the whole Club Grid locally, with docker, so that it loads clubs and conditions to the database
2. Run `scripts/validate_conditions.py` which will print a table to the terminal with a report, including # solutions, errors, etc.