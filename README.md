# Python Engineering Foundation Class (pefc) Library

Library to perform engineering data analysis using python.
Currently the completed module is xltab which contain classes that tabulate data from MS Excel forms.
It is a common practice to use MS Excel as a 'form' for operators to enter data in a typical shopfloor. Extracting data for analysis from many such forms is a pain which xltab tries to solve. A directory may contain from hundreds to thousands of such MS Excel files typically saved by batch numbers.
With xltab you can collect data from multiple MS Excel files and save it into a tabular format that pandas.read_excel() function can read. You can also collect the data and convert it to pandas.DataFrame().
You can then use the powerful Pandas package to perform your data analysis.

xltab makes use of three common Excel related packages to read/write data from your Excel file.
They are xlrd, openpyxl, xlwings and theie respective xltab classes are XLDataLink, OXLDataLink and XLWDataLink.
Why these three packages? Each have their pros amd cons. xlrd can read both xls and xlsx files but cannot write.
XLDataLink which uses xlrd is best to use if you only want to read data. XLDataLink makes use of cell references e.g. 'A10' instead of row number and column number so it is more convenient to use than xlrd.
openpyxl only works with the newer xlsx MS Excel files but can read and write.
xlwings needs MS Excel installed into your computer to work.
If you find that OXLDataLink is not suitable for your files then you can easily switch to XLDataLink or XLWDataLink. XLWDataLink is the slowest because it uses MS Excel to read and write your Excel files but it has one advantage the others don't have.  MS Excel is excellent in handling files that have format issues seamlessly.
XLWDatalink solves some workbook errors such as:'xlrd.biffh.XLRDError: Workbook is encrypted' caused by MS Excel 95 protected file issue. It can fix formula errors on the fly using xlwings.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

## Deployment

WIP

## Built With

* python.org

## Contributing

Please read for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use git for versioning.

## Authors

* **Heng Swee Ngee** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc