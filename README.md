Data2libFormat
======
A simple tool for converting csv data into [libSVM](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)/[libFM](http://www.libfm.org/) format.

Usage
======
```python
python main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]
```

To speed up data processing, it supports [pypy](http://pypy.org/) as well. 
```python
pypy main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]
```

For more details, plase refer to `--help` function.
```python
python main.py --help
```

An Example
======
For a csv data:
```csv
rating::user::item::age
9::userA::itemA::18
4::userA::itemB::16
5::userB::itemB::29
```
By using following instruction: 
```python
python main.py -task 'csv2lib' -infile [InputFile] -ofile [Outputfile] -target 0 -cat 1,2 -num 3 -sep '::'
```
It's able to get a converted data with libSVM-like format.
```csv
9 1:1 3:1 5:18
4 1:1 4:1 5:16
5 2:1 4:1 5:29
```
