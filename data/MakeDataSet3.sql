create table dataset_wx_final
select a.date, a.oneDayBefore, a.twoDayBefore, b.price threeDayBefore ,a.oneMonthBefore, a.oneYearBefore, a.dollorRate, a.price
from dataset_wx_2 as a left join price_1 as b 
on a.date=b.date + interval 3 day
order by 1;