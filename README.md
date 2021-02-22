MySQL workshop, October 14

In this workshop, we will learn some basic SQL commands:
* Parse CSV files and construct tables out of them
* Query data in and across tables
* Insert, delete, and update entries
* Alter tables
* Export data

Prerequisites for this workshop:

* Networking: you will need to be logged into the Rice network
	* Either log in to the Rice Owls wifi
	* Or log into VPN, following these instructions: https://kb.rice.edu/page.php?id=82263
* MySQL software: One of the following
	* RECOMMENDED: MySQL Workbench: https://dev.mysql.com/doc/workbench/en/
	* NO GUARANTEES: A command-line interface
		* Brew CLI: https://formulae.brew.sh/formula/mysql-client
* Text editing software: you will need a basic text editor
	* I recommend BBEdit: https://www.barebones.com/products/bbedit/
* Data:
	* We will be working with the Certified 2019 property data export from Fort Bend County
	* https://www.fbcad.org/certified-and-supplements-reports/

Tentative Outline: 

1. open sql workbench
1. connect to vpn (cisco/duo)
1. connect to remote database
1. show that we've got nothing in there but system stuff (show databases)
1. create database command
1. what goes into databases? tables
1. but what do these tables look like? what kind of data are we working with?
1. introduce dataset (county appraiser's website)
1. pull, unzip, and examine dataset (and show the network setup I'm using to do this)
https://www.fbcad.org/certified-and-supplements-reports/
1. csv headers, excel layout, back to csv headers. create tables
https://dev.mysql.com/doc/refman/8.0/en/create-table.html
1. mysqlimport (land, owner, property)
https://dev.mysql.com/doc/refman/8.0/en/mysqlimport.html
1. examine records in the three tables -- structure, relationship
1. alter table owner drop OwnerName -- but we've still got unique identifiers -- no foreign key constraints (can't trust that these won't fail and create issues without well-cleaned data)
--this is basic anonymization -- but remember there's no such thing as anonymization
1. commands: count, distinct, limit
1. commands: where (like, =, in), order by (random, prop value...)
1. commands: join (and maybe show them outer join)
https://dev.mysql.com/doc/refman/8.0/en/join.html
1. aliases (table as X, string as Y)
1. commands: group by
1. views -- pre-baked query in mysqlworkbench
1. there's also the insert into table select....
https://dev.mysql.com/doc/refman/8.0/en/ansi-diff-select-into-table.html
1. but we favor the "into outfile" dump for our purposes, because we know that having these exports on hand is a major accomplishment in the project. we can save these old databases, but we're really going to be working with the cleaned data. https://dev.mysql.com/doc/refman/8.0/en/select-into.html https://dev.mysql.com/doc/refman/5.6/en/mysql-batch-commands.html
1. get create table syntax from our export. mysqlimport for that file.
1. appendix:
	1. python connectors
		1. https://dev.mysql.com/doc/connector-python/en/
		1. https://docs.python.org/3/library/sqlite3.html
	1. sqlite
		1. can share my Herschel files to this end
	1. sv data
