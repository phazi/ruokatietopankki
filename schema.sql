--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)


--
-- Name: food_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE food_stats (
    foodid SERIAL PRIMARY KEY,
    foodname text,
    energia_laskennallinen numeric,
    rasva numeric,
    hiilihydraatti_imeytyva numeric,
    hiilihydraatti_erotuksena numeric,
    proteiini numeric,
    alkoholi numeric,
    tuhka numeric,
    vesi numeric,
    kcal numeric(28,1) GENERATED ALWAYS AS ((energia_laskennallinen * 0.239)) STORED
);


--
-- Name: recipe_foods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE recipe_foods (
    id SERIAL PRIMARY KEY,
    recipeid integer,
    foodid integer,
    amount numeric(18,2)
);



--
-- Name: user_fav_foods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_fav_foods (
    id SERIAL PRIMARY KEY,
    userid integer,
    foodid integer,
    created_ts timestamp without time zone,
    active BOOLEAN NOT NULL DEFAULT TRUE
);


--
-- Name: user_recipes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_recipes (
    recipeid SERIAL PRIMARY KEY,
    userid integer NOT NULL,
    name text NOT NULL,
    description text,
    created_ts timestamp without time zone NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username text NOT NULL,
    password text
);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: user_profiles fk_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_profiles
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);

--
-- Name: recipe_foods recipe_foods_foodid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY recipe_foods
    ADD CONSTRAINT recipe_foods_foodid_fkey FOREIGN KEY (foodid) REFERENCES food_stats(foodid);


--
-- Name: recipe_foods recipe_foods_recipeid_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY recipe_foods
    ADD CONSTRAINT recipe_foods_recipeid_fk FOREIGN KEY (recipeid) REFERENCES user_recipes(recipeid);


--
-- Name: user_fav_foods user_fav_foods_foodid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_fav_foods
    ADD CONSTRAINT user_fav_foods_foodid_fkey FOREIGN KEY (foodid) REFERENCES food_stats(foodid);


--
-- Name: user_fav_foods user_fav_foods_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_fav_foods
    ADD CONSTRAINT user_fav_foods_userid_fkey FOREIGN KEY (userid) REFERENCES users(id);


--
-- Name: user_recipes user_recipes_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_recipes
    ADD CONSTRAINT user_recipes_userid_fkey FOREIGN KEY (userid) REFERENCES users(id);


