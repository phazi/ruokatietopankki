CREATE TABLE public.food_stats (
    foodid integer NOT NULL,
    foodname text,
    energia_laskennallinen numeric,
    rasva numeric,
    hiilihydraatti_imeytyva numeric,
    hiilihydraatti_erotuksena numeric,
    proteiini numeric,
    alkoholi numeric,
    tuhka numeric,
    vesi numeric
);

alter table food_stats add constraint food_stats_pkey primary key (foodid);