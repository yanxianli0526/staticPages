DB_HOST=localhost
DB_PORT=3306
DB_USER=test
DB_PASSWARD=test
DB_DATABASE=localTest2
export DB_HOST DB_PORT DB_USER DB_PASSWARD DB_DATABASE

local-run:
	python3 businessDistrict.py 

run:
	python businessDistrict.py 