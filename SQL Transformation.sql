SELECT * FROM calldetails;
SELECT * FROM calllog;

--- Total Number of Calls Resolved vs Total Number of Calls Received

WITH call_resolved AS
(
SELECT DISTINCT agentid,COUNT(callerid) AS no_of_calls_resolved
FROM calllog
WHERE status = 'resolved'
GROUP BY 1
),
calls_received AS
(
SELECT DISTINCT agentid, COUNT(callerid) no_of_calls_received
FROM calllog
GROUP BY 1	
)

SELECT a.agentid, no_of_calls_resolved,no_of_calls_received FROM call_resolved a
JOIN calls_received b 
ON a.agentid = b.agentid;


INSERT INTO total_calls
(

agentid,
no_of_calls_resolved ,
no_of_calls_received 	
)
WITH call_resolved AS
(
SELECT DISTINCT agentid,COUNT(callerid) AS no_of_calls_resolved
FROM calllog
WHERE status = 'resolved'
GROUP BY 1
),
calls_received AS
(
SELECT DISTINCT agentid, COUNT(callerid) no_of_calls_received
FROM calllog
GROUP BY 1	
)

SELECT a.agentid, no_of_calls_resolved,no_of_calls_received FROM call_resolved a
JOIN calls_received b 
ON a.agentid = b.agentid;

CREATE TABLE IF NOT EXISTS  total_calls
(
id	INTEGER PRIMARY KEY NOT NULL,
agentid		INTEGER,
no_of_calls_resolved	BIGINT,
no_of_calls_received	BIGINT
);	

-- Total Number of calls received vs Total Number of calls assigned/resolved

WITH calls_received AS
(
SELECT DISTINCT agentid, COUNT(callerid) no_of_calls_received
FROM calllog
GROUP BY 1	
),
calls_assigned AS
(
SELECT DISTINCT agentid, COUNT(callerid) no_of_calls_assigned
FROM calllog
WHERE agentid <> assignedto	
GROUP BY 1	
),

call_resolved AS
(
SELECT DISTINCT agentid,COUNT(callerid) AS no_of_calls_resolved
FROM calllog
WHERE status = 'resolved'
GROUP BY 1
)
SELECT a.agentid,no_of_calls_received,no_of_calls_assigned,no_of_calls_resolved 
FROM calls_received a
JOIN calls_assigned b 
ON a.agentid = b.agentid
LEFT JOIN call_resolved c
ON a.agentid = c.agentid;

--The total and average call duration for each agent, and the grade level of 
--these agents.


SELECT DISTINCT agentid, agentsgradelevel, 
SUM(calldurationinseconds) over (PARTITION BY agentid) AS total_call_duration,
AVG (calldurationinseconds) over (PARTITION BY agentid) AS avg_call_duration
FROM calllog a JOIN calldetails b on CAST (id as varchar) = callid

CREATE TABLE IF NOT EXISTS dim_call_duration
(
id	INTEGER PRIMARY KEY NOT NULL,
agentid		INTEGER,
agentsgradelevel CHARACTER VARYING(100),
total_call_duration BIGINT,
avg_call_duration BIGINT  	
);	

--The earliest and latest closed and resolved calls, and the grade levels of the 
--agents who resolved these cases.

SELECT * FROM calldetails
SELECT * FROM calllog;

SELECT DISTINCT agentid, agentsgradelevel,status,
COUNT(*) over (PARTITION BY agentid) AS total_calls
FROM calllog a JOIN calldetails b on cast (id as varchar) = callid
WHERE status IN ( 'resolved','closed')
ORDER BY status;

CREATE TABLE IF NOT EXISTS dim_call_status
(
id	INTEGER PRIMARY KEY NOT NULL,
agentid		INTEGER,
agentsgradelevel CHARACTER VARYING(100),
status CHARACTER VARYING(50),
total_calls BIGINT  	
);	

CREATE TABLE IF NOT EXISTS ft_call_details
(
id	BIGINT IDENTITY(1, 1),
agentid		INTEGER,
callid CHARACTER VARYING(100),
no_of_calls_received BIGINT,	
status CHARACTER VARYING(50),
calltype CHARACTER VARYING(50),
callendedbyagent BOOLEAN,	
calldurationinseconds INTEGER,
resolutiondurationinhours CHARACTER VARYING(20) 	
);	

SELECT DISTINCT agentid,callid, COUNT(callerid) over (PARTITION BY agentid) no_of_calls_received,status,
calltype,callendedbyagent,calldurationinseconds,resolutiondurationinhours
FROM calllog a JOIN calldetails
ON CAST (id  AS VARCHAR) = callid


SELECT * FROM calllog 
SELECT * FROM calldetails