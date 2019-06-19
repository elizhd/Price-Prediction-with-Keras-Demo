create table price_3_demo
select a.date,a.price,a.oneDayBefore, b.price as oneMonthBefore 
from price_2 as a left join price_1 as b on a.date=(b.date+ interval  1 MONTH) order by 1;