
## DESCRIPTION
WeServe is a call service agency that outsources customer service personnels to several companies.
The Purpose of this project is to conduct data cleaning,data extraction,transformation and loading of Weserve data from Database to a data warehouse using AWS.

## TOOLS USED
-PostgreSql
-Pandas
-AWS Data Lake (S3 Bucket)
-AWS Data Warehouse (Redshift Service)
-Python
-Boto3
-sqlalchemy

## RESULTING WAREHOUSE SCHEMA

### 1. dim_total_calls 
agentid		INTEGER,
no_of_calls_resolved BIGINT,
no_of_calls_received BIGINT,
no_of_calls_assigned BIGINT  	


### 2. dim_call_duration 
agentid		INTEGER,
agentsgradelevel CHARACTER VARYING(100),
total_call_duration BIGINT,
avg_call_duration BIGINT  	


### 3. dim_call_status 
agentid		INTEGER,
agentsgradelevel CHARACTER VARYING(100),
status CHARACTER VARYING(50),
total_calls BIGINT  	

### 4. ft_call_details
agentid		INTEGER,
callid CHARACTER VARYING(100),
no_of_calls_received BIGINT,	
status CHARACTER VARYING(50),
calltype CHARACTER VARYING(50),
callendedbyagent BOOLEAN,	
calldurationinseconds INTEGER,
resolutiondurationinhours CHARACTER VARYING(20) 	



## STEP BY STEP PROCESSES
### Understanding the datasets.
- creating a new database called weserve on postgres.
- create 2 different tables to house the 2 datasets given
- importing the datasets into the 2 tables created.

### Cleaning the datasets
- create copy of the tables 
- cleaned Columns with dirty data; callid( change agentgradelevel to 1) & calltype(change in-bound to inbound to align with other parameters) on call details and assignedTo(change null values to the corresponding agentid), resolutiondurationinhours(change null values to NA) & status(correct the case sensitivity to align) on call log.

### Deriving and Creating the transformed datasets(dimensions and fact)
- fact : call details
- dimension : call status
- dimension : call duration
- dimension : total calls

### Environment Setup
- Create Virtual Environment.
- Activate the environment.
- Install all required packages; pandas, psycopg2, sqlalchemy, s3fs, boto3, configparser.
- Create user on AWS(IAM) ; add policy to the user, create access key and get secret key.

### ETL Process
- Create S3 Bucket(datalake) using access key, secret key and desired region and bucket name.
- Extract data from database(postgres) to datalake(S3)
- Create a Redshift severless cluster.
- Loading into initial schema(dev schema); create dev schema, create tables.
- copy tables from S3(datalake) to redshift(data warehouse) (into the dev schema)
- create final/resulting schema (staging schema).
- create star schema tables(fact and dimensions)
- insert the data into facts and dimensions.



## RESULTS OF THE KPI MEASURES

### 1. Total Number of Calls Resolved vs Total Number of Calls Received.
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

### 2. Total Number of calls received vs Total Number of calls assigned/resolved
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
; 

### 3. The total and average call duration for each agent, and the grade level of these agents

SELECT DISTINCT agentid, agentsgradelevel, 
SUM(calldurationinseconds) over (PARTITION BY agentid) AS total_call_duration,
AVG (calldurationinseconds) over (PARTITION BY agentid) AS avg_call_duration
FROM dev.calllog a JOIN dev.calldetails b on CAST (id as varchar) = callid
;

### 4. The earliest and latest closed and resolved calls, and the grade levels of the agents who resolved these cases

SELECT DISTINCT agentid, agentsgradelevel,status,
COUNT(*) over (PARTITION BY agentid) AS total_calls
FROM dev.calllog a JOIN dev.calldetails b on cast (id as varchar) = callid
WHERE status IN ( 'resolved','closed') 
ORDER BY status
;
