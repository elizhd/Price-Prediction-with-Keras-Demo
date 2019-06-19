create table price_2
select a.date,a.price, b.price as oneDayBefore 
from price_1 as a left join price_1 as b on a.date = b.date + interval 1 day;