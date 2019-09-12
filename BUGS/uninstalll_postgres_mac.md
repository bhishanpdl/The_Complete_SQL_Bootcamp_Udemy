# To uninstall postgres10 and postgres11 on mac
On my laptop I have postgres10 installed from official website .dmg file and postgres11 installed from brew.
- postgres11 could not install dvdrental.tar so it is useless.
- postgres10 was able to install dvdrental.tar (pgadmin could open staff table, but psycopg2 juyternotebook
  can not open staff table)
- I tried dropping the database dvdrental from pgadmin and install from tar file of corrected dat file.
- All options failed
  + original dvdrental_corrupted.tar failed
  + corrected dvdrental.tar failed.
  + I download the dvdrental.tar from course website and tried to intall using pgadmin, it failed.
- On date Sep 11, 2019, I decided to uninstall both, and fresh install only postgres10.

# uninstallation
```bash
# 11
brew uninstall --ignore-dependencies postgresql

# 10
 cd /Library/PostgreSQL/
 
 cd 10
 open uninstall-postgresql.app/
 sudo rm -rf 11
 
 cd 10/
 sudo open uninstall-postgresql.app
 
 cd /Applications/
 cd PostgreSQL\ 10/
```

# Re install
Date: Sep 12, 2019

## attempt1 10.10 installer (failed)
- download macos installer for 10.10 from https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1256720
- This downloads a dmg file, double click to install it
- Choose default options (course video suggested to uncheck pgadmin4 and install it separately, however I tried default).

Got error:
```
Problem running post-install step. Installation may not complete correctly
 The database cluster initialisation failed.
```

This failed miserably, could not create any database from pgadmin. Unistalled again.

## attempt2 using brew (failed)
https://medium.com/@bitadj/completely-uninstall-and-reinstall-psql-on-osx-551390904b86
```
brew install postgres
$ createdb `whoami`
createdb: could not connect to database template1: could not connect to server: No such file or directory
	Is the server running locally and accepting
	connections on Unix domain socket "/tmp/.s.PGSQL.5432"?
```

### attempt3 11.5 installer and pgadmin separately
- first installed pgadmin4 to applications, gives no error
- installed 11.5, unchecked pgadmin4 option, gives no error.
- tried to create database from dvdrental.tar file, gives error.
- restarted the pgadmig, gives the database but tables are empty.
- dropped the dvdrental database.
- tried to create database from restore.sql, but also failed.
- Restarted pgadmin, it gives error, but IT WORKS.
- open Query tool in pgadmin and type `select * from customer limit 5;` hit F5, it runs. GOOD!!!

