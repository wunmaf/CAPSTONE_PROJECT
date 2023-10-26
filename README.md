
## DESCRIPTION
WeServe is a call service agency that outsources customer service personnels to several companies.
This Porpose of this project is to conduct data cleaning,data extraction,transformation and loading of Weserve data from Database to a data warehouse using AWS.

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


## RESULTS OF THE KPI MEASURES
