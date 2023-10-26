
dim_total_calls = ''' 
WITH calls_received AS
(
SELECT DISTINCT agentid, COUNT(callerid) no_of_calls_received
FROM dev.calllog
GROUP BY 1	
),
calls_assigned AS
(
SELECT DISTINCT agentid, COUNT(callerid) no_of_calls_assigned
FROM dev.calllog
WHERE agentid <> assignedto	
GROUP BY 1	
),

call_resolved AS
(
SELECT DISTINCT agentid,COUNT(callerid) AS no_of_calls_resolved
FROM dev.calllog
WHERE status = 'resolved'
GROUP BY 1
)
SELECT a.agentid,no_of_calls_received,no_of_calls_assigned,no_of_calls_resolved 
FROM calls_received a
JOIN calls_assigned b 
ON a.agentid = b.agentid
LEFT JOIN call_resolved c
ON a.agentid = c.agentid;
; '''


dim_call_duration = '''INSERT INTO staging.dim_call_duration
(

agentid,		
agentsgradelevel,
total_call_duration,
avg_call_duration   	
)
SELECT DISTINCT agentid, agentsgradelevel, 
SUM(calldurationinseconds) over (PARTITION BY agentid) AS total_call_duration,
AVG (calldurationinseconds) over (PARTITION BY agentid) AS avg_call_duration
FROM dev.calllog a JOIN dev.calldetails b on CAST (id as varchar) = callid
;'''


dim_call_status = '''
INSERT INTO dim_call_status
(
agentid,
agentsgradelevel,
status,
total_calls 	
)

SELECT DISTINCT agentid, agentsgradelevel,status,
COUNT(*) over (PARTITION BY agentid) AS total_calls
FROM dev.calllog a JOIN dev.calldetails b on cast (id as varchar) = callid
WHERE status IN ( 'resolved','closed') 
ORDER BY status
;'''	

ft_call_details = '''INSERT INTO staging.ft_call_details(
agentid,		
callid,
no_of_calls_received,	
status,
calltype,
callendedbyagent,	
calldurationinseconds,
resolutiondurationinhours 	
)

SELECT DISTINCT agentid,callid, COUNT(callerid) over (PARTITION BY agentid) no_of_calls_received,status,
calltype,callendedbyagent,calldurationinseconds,resolutiondurationinhours
FROM dev.calllog a JOIN dev.calldetails
ON CAST (id  AS VARCHAR) = callid
;'''


transformation_queries = [dim_total_calls, dim_call_duration, dim_call_status, ft_call_details]