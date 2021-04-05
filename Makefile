SRC_DB = cpad
DEST_DB = cpad2

run: copy
	./export.py # -s 1

install:
	python3 -m pip install -r requirements.txt	

orm:
	pwiz.py $(SRC_DB) > src_db.py

copy:
	./copy_db.sh $(SRC_DB) $(DEST_DB)
