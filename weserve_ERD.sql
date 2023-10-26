CREATE TABLE "dim_call_status"(
    "id" BIGINT NOT NULL,
    "agentid" INTEGER NOT NULL,
    "agentsgradelevel" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "total_calls" BIGINT NULL
);
ALTER TABLE
    "dim_call_status" ADD PRIMARY KEY("id");
CREATE TABLE "dim_total_calls"(
    "id" BIGINT NOT NULL,
    "agentid" INTEGER NULL,
    "no_of_calls_resolved" BIGINT NOT NULL,
    "no_of_calls_received" BIGINT NOT NULL,
    "no_of_calls_assigned" BIGINT NOT NULL
);
ALTER TABLE
    "dim_total_calls" ADD PRIMARY KEY("id");
CREATE TABLE "dim_call_duration"(
    "id" BIGINT NOT NULL,
    "agentid" INTEGER NOT NULL,
    "agentsgradelevel" VARCHAR(255) NOT NULL,
    "total_call_duration" BIGINT NULL,
    "avg_call_duration" BIGINT NULL
);
ALTER TABLE
    "dim_call_duration" ADD PRIMARY KEY("id");
CREATE TABLE "ft_call_details"(
    "id" BIGINT NOT NULL,
    "agentid" INTEGER NOT NULL,
    "callid" VARCHAR(255) NOT NULL,
    "no_of_calls_received" BIGINT NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "calltype" VARCHAR(255) NOT NULL,
    "callendedbyagent" BOOLEAN NOT NULL,
    "calldurationinseconds" INTEGER NOT NULL,
    "resolutiondurationinhours" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "ft_call_details" ADD PRIMARY KEY("id");
ALTER TABLE
    "dim_total_calls" ADD CONSTRAINT "dim_total_calls_agentid_foreign" FOREIGN KEY("agentid") REFERENCES "ft_call_details"("agentid");
ALTER TABLE
    "ft_call_details" ADD CONSTRAINT "ft_call_details_agentid_foreign" FOREIGN KEY("agentid") REFERENCES "dim_call_status"("agentid");
ALTER TABLE
    "ft_call_details" ADD CONSTRAINT "ft_call_details_agentid_foreign" FOREIGN KEY("agentid") REFERENCES "dim_call_duration"("agentid");