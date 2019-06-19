create table price_4
select a.date, a.price, a.oneDayBefore, a.oneMonthBefore, b.price as oneYearBefore
from price_3 as a left join price_1 as b on a.date=(b.date+ interval  1 Year ) order by 1;