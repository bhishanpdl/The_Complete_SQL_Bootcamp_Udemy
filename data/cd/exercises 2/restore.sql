--
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = cd, pg_catalog;

ALTER TABLE ONLY cd.members DROP CONSTRAINT fk_members_recommendedby;
ALTER TABLE ONLY cd.bookings DROP CONSTRAINT fk_bookings_memid;
ALTER TABLE ONLY cd.bookings DROP CONSTRAINT fk_bookings_facid;
DROP INDEX cd."members.recommendedby";
DROP INDEX cd."members.joindate";
DROP INDEX cd."bookings.starttime";
DROP INDEX cd."bookings.memid_starttime";
DROP INDEX cd."bookings.memid_facid";
DROP INDEX cd."bookings.facid_starttime";
DROP INDEX cd."bookings.facid_memid";
ALTER TABLE ONLY cd.members DROP CONSTRAINT members_pk;
ALTER TABLE ONLY cd.facilities DROP CONSTRAINT facilities_pk;
ALTER TABLE ONLY cd.bookings DROP CONSTRAINT bookings_pk;
DROP TABLE cd.members;
DROP TABLE cd.facilities;
DROP TABLE cd.bookings;
DROP SCHEMA cd;
--
-- Name: cd; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA cd;


ALTER SCHEMA cd OWNER TO postgres;

SET search_path = cd, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: bookings; Type: TABLE; Schema: cd; Owner: postgres
--

CREATE TABLE bookings (
    bookid integer NOT NULL,
    facid integer NOT NULL,
    memid integer NOT NULL,
    starttime timestamp without time zone NOT NULL,
    slots integer NOT NULL
);


ALTER TABLE bookings OWNER TO postgres;

--
-- Name: facilities; Type: TABLE; Schema: cd; Owner: postgres
--

CREATE TABLE facilities (
    facid integer NOT NULL,
    name character varying(100) NOT NULL,
    membercost numeric NOT NULL,
    guestcost numeric NOT NULL,
    initialoutlay numeric NOT NULL,
    monthlymaintenance numeric NOT NULL
);


ALTER TABLE facilities OWNER TO postgres;

--
-- Name: members; Type: TABLE; Schema: cd; Owner: postgres
--

CREATE TABLE members (
    memid integer NOT NULL,
    surname character varying(200) NOT NULL,
    firstname character varying(200) NOT NULL,
    address character varying(300) NOT NULL,
    zipcode integer NOT NULL,
    telephone character varying(20) NOT NULL,
    recommendedby integer,
    joindate timestamp without time zone NOT NULL
);


ALTER TABLE members OWNER TO postgres;

--
-- Data for Name: bookings; Type: TABLE DATA; Schema: cd; Owner: postgres
--

COPY bookings (bookid, facid, memid, starttime, slots) FROM stdin;
\.
COPY bookings (bookid, facid, memid, starttime, slots) FROM '$$PATH$$/2386.dat';

--
-- Data for Name: facilities; Type: TABLE DATA; Schema: cd; Owner: postgres
--

COPY facilities (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance) FROM stdin;
\.
COPY facilities (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance) FROM '$$PATH$$/2387.dat';

--
-- Data for Name: members; Type: TABLE DATA; Schema: cd; Owner: postgres
--

COPY members (memid, surname, firstname, address, zipcode, telephone, recommendedby, joindate) FROM stdin;
\.
COPY members (memid, surname, firstname, address, zipcode, telephone, recommendedby, joindate) FROM '$$PATH$$/2388.dat';

--
-- Name: bookings_pk; Type: CONSTRAINT; Schema: cd; Owner: postgres
--

ALTER TABLE ONLY bookings
    ADD CONSTRAINT bookings_pk PRIMARY KEY (bookid);


--
-- Name: facilities_pk; Type: CONSTRAINT; Schema: cd; Owner: postgres
--

ALTER TABLE ONLY facilities
    ADD CONSTRAINT facilities_pk PRIMARY KEY (facid);


--
-- Name: members_pk; Type: CONSTRAINT; Schema: cd; Owner: postgres
--

ALTER TABLE ONLY members
    ADD CONSTRAINT members_pk PRIMARY KEY (memid);


--
-- Name: bookings.facid_memid; Type: INDEX; Schema: cd; Owner: postgres
--

CREATE INDEX "bookings.facid_memid" ON bookings USING btree (facid, memid);


--
-- Name: bookings.facid_starttime; Type: INDEX; Schema: cd; Owner: postgres
--

CREATE INDEX "bookings.facid_starttime" ON bookings USING btree (facid, starttime);


--
-- Name: bookings.memid_facid; Type: INDEX; Schema: cd; Owner: postgres
--

CREATE INDEX "bookings.memid_facid" ON bookings USING btree (memid, facid);


--
-- Name: bookings.memid_starttime; Type: INDEX; Schema: cd; Owner: postgres
--

CREATE INDEX "bookings.memid_starttime" ON bookings USING btree (memid, starttime);


--
-- Name: bookings.starttime; Type: INDEX; Schema: cd; Owner: postgres
--

CREATE INDEX "bookings.starttime" ON bookings USING btree (starttime);


--
-- Name: members.joindate; Type: INDEX; Schema: cd; Owner: postgres
--

CREATE INDEX "members.joindate" ON members USING btree (joindate);


--
-- Name: members.recommendedby; Type: INDEX; Schema: cd; Owner: postgres
--

CREATE INDEX "members.recommendedby" ON members USING btree (recommendedby);


--
-- Name: fk_bookings_facid; Type: FK CONSTRAINT; Schema: cd; Owner: postgres
--

ALTER TABLE ONLY bookings
    ADD CONSTRAINT fk_bookings_facid FOREIGN KEY (facid) REFERENCES facilities(facid);


--
-- Name: fk_bookings_memid; Type: FK CONSTRAINT; Schema: cd; Owner: postgres
--

ALTER TABLE ONLY bookings
    ADD CONSTRAINT fk_bookings_memid FOREIGN KEY (memid) REFERENCES members(memid);


--
-- Name: fk_members_recommendedby; Type: FK CONSTRAINT; Schema: cd; Owner: postgres
--

ALTER TABLE ONLY members
    ADD CONSTRAINT fk_members_recommendedby FOREIGN KEY (recommendedby) REFERENCES members(memid) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

