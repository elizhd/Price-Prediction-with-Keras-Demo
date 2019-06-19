create table avg_dollor_rate
SELECT date_format(发布日期,'%Y-%m-%d') date, avg(中行折算价) avgRate 
FROM `database`.dollor_rate_raw
WHERE 发布日期>='2014-01-01' and 发布日期<='2018-12-31'
group by date;