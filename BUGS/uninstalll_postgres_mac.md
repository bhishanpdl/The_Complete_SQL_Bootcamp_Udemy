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
