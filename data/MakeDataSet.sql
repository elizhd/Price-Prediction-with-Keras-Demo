create table dataset_wx_1
select a.date, a.oneDayBefore, a.oneMonthBefore, a.oneYearBefore, b.avgRate as dollorRate, a.price
from price_4 as a left join avg_dollor_rate as b 
on a.date=b.date + interval 1 day
order by 1;