create table price_today
select b.date date, a.price price
from test1 as a right join list_date as b on a.date = b.date;