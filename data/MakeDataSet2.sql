create table dataset_wx_2
select a.date, a.oneDayBefore, b.price twoDayBefore ,a.oneMonthBefore, a.oneYearBefore, a.dollorRate, a.price
from dataset_wx_1 as a left join price_1 as b 
on a.date=b.date + interval 2 day
order by 1;