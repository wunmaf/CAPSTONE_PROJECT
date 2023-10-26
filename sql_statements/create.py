# =============================================== FOR DEV SCHEMA
calldetails = '''CREATE TABLE IF NOT EXISTS dev.calldetails
(
callid	CHARACTER VARYING(100) PRIMARY KEY NOT NULL,
callDurationInSeconds	INTEGER,
agentsGradeLevel	CHARACTER VARYING(100),
callType	CHARACTER VARYING(100),
callEndedByAgent	BOOLEAN
);'''

calllog = '''CREATE TABLE IF NOT EXISTS dev.calllog
(
id	INTEGER PRIMARY KEY NOT NULL,
callerID		CHARACTER VARYING (100),
agentID	INTEGER,	
complaintTopic	TEXT,
assignedTo	INTEGER,
status	CHARACTER VARYING (50),
resolutionDurationInHours 	CHARACTER VARYING(20)
);'''

# =============================================== FOR STAR SCHEMA

dim_total_calls = ''' CREATE TABLE IF NOT EXISTS staging.dim_total_calls
(

agentid		INTEGER,
no_of_calls_resolved BIGINT,
no_of_calls_received BIGINT,
no_of_calls_assigned BIGINT  	
); '''

dim_call_duration = '''CREATE TABLE IF NOT EXISTS staging.dim_call_duration
(

agentid		INTEGER,
agentsgradelevel CHARACTER VARYING(100),
total_call_duration BIGINT,
avg_call_duration BIGINT  	
);'''

dim_call_status = '''CREATE TABLE IF NOT EXISTS staging.dim_call_status
(
agentid		INTEGER,
agentsgradelevel CHARACTER VARYING(100),
status CHARACTER VARYING(50),
total_calls BIGINT  	
);'''

ft_call_details = '''CREATE TABLE IF NOT EXISTS staging.ft_call_details
(

agentid		INTEGER,
callid CHARACTER VARYING(100),
no_of_calls_received BIGINT,	
status CHARACTER VARYING(50),
calltype CHARACTER VARYING(50),
callendedbyagent BOOLEAN,	
calldurationinseconds INTEGER,
resolutiondurationinhours CHARACTER VARYING(20) 	
);	'''



dev_tables = [calldetails,calllog]
transformed_tables = [dim_total_calls, dim_call_duration, dim_call_status, ft_call_details]