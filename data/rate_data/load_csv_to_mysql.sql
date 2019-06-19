// mysql --local-infile -u root -p
load data local infile 'E:/InnovateProject/data/rate_data/2018_M07-M12_rate.csv'
into table dollor_rate
FIELDS TERMINATED BY ',';
// IGNORE 1 LINES;

