# staff table of database dvdrental is corrupted 
The data file `2187.dat` corresponding to `staff` table is corrupted.

```
1	Mike	Hillyer	3	Mike.Hillyer@sakilastaff.com	1	t	Mike	8cb2237d0679ca88db6464eac60da96345513964	2006-05-16 16:13:11.79328	\\x89504e470d0a5a0a
2	Jon	Stephens	4	Jon.Stephens@sakilastaff.com	2	t	Jon	8cb2237d0679ca88db6464eac60da96345513964	2006-05-16 16:13:11.79328	\N
\.
```

We can see third line is \. and it gives the problem.


# command 
```sql
%%sql
select * from staff;
```

# Error
```bash
* postgres://postgres:***@localhost:5433/dvdrental
2 rows affected.
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
~/miniconda3/envs/dataSc/lib/python3.7/site-packages/IPython/core/formatters.py in __call__(self, obj)
    343             method = get_real_method(obj, self.print_method)
    344             if method is not None:
--> 345                 return method()
    346             return None
    347         else:

~/miniconda3/envs/dataSc/lib/python3.7/site-packages/sql/run.py in _repr_html_(self)
    127         if self.pretty:
    128             self.pretty.add_rows(self)
--> 129             result = self.pretty.get_html_string()
    130             result = _cell_with_spaces_pattern.sub(_nonbreaking_spaces, result)
    131             if self.config.displaylimit and len(

~/miniconda3/envs/dataSc/lib/python3.7/site-packages/prettytable.py in get_html_string(self, **kwargs)
   1184             string = self._get_formatted_html_string(options)
   1185         else:
-> 1186             string = self._get_simple_html_string(options)
   1187 
   1188         return string

~/miniconda3/envs/dataSc/lib/python3.7/site-packages/prettytable.py in _get_simple_html_string(self, options)
   1214 
   1215         # Data
-> 1216         rows = self._get_rows(options)
   1217         formatted_rows = self._format_rows(rows, options)
   1218         for row in formatted_rows:

~/miniconda3/envs/dataSc/lib/python3.7/site-packages/prettytable.py in _get_rows(self, options)
    924 
    925         # Make a copy of only those rows in the slice range
--> 926         rows = copy.deepcopy(self._rows[options["start"]:options["end"]])
    927         # Sort if necessary
    928         if options["sortby"]:

~/miniconda3/envs/dataSc/lib/python3.7/copy.py in deepcopy(x, memo, _nil)
    148     copier = _deepcopy_dispatch.get(cls)
    149     if copier:
--> 150         y = copier(x, memo)
    151     else:
    152         try:

~/miniconda3/envs/dataSc/lib/python3.7/copy.py in _deepcopy_list(x, memo, deepcopy)
    213     append = y.append
    214     for a in x:
--> 215         append(deepcopy(a, memo))
    216     return y
    217 d[list] = _deepcopy_list

~/miniconda3/envs/dataSc/lib/python3.7/copy.py in deepcopy(x, memo, _nil)
    148     copier = _deepcopy_dispatch.get(cls)
    149     if copier:
--> 150         y = copier(x, memo)
    151     else:
    152         try:

~/miniconda3/envs/dataSc/lib/python3.7/copy.py in _deepcopy_list(x, memo, deepcopy)
    213     append = y.append
    214     for a in x:
--> 215         append(deepcopy(a, memo))
    216     return y
    217 d[list] = _deepcopy_list

~/miniconda3/envs/dataSc/lib/python3.7/copy.py in deepcopy(x, memo, _nil)
    167                     reductor = getattr(x, "__reduce_ex__", None)
    168                     if reductor:
--> 169                         rv = reductor(4)
    170                     else:
    171                         reductor = getattr(x, "__reduce__", None)

TypeError: can't pickle memoryview objects

[(1, 'Mike', 'Hillyer', 3, 'Mike.Hillyer@sakilastaff.com', 1, True, 'Mike', '8cb2237d0679ca88db6464eac60da96345513964', datetime.datetime(2006, 5, 16, 16, 13, 11, 793280), <memory at 0x1144f5d08>),
 (2, 'Jon', 'Stephens', 4, 'Jon.Stephens@sakilastaff.com', 2, True, 'Jon', '8cb2237d0679ca88db6464eac60da96345513964', datetime.datetime(2006, 5, 16, 16, 13, 11, 793280), None)]
```
