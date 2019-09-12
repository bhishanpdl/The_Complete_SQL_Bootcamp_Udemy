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
- download macos installer for 10.10 from https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1256720
