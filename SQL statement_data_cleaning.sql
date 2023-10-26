select * from call_details;
select * from calldetails;

CREATE TABLE calldetails AS
SELECT * FROM call_details;

CREATE TABLE calllog AS
SELECT * FROM call_log;

-- data cleaning on call details
UPDATE  calldetails
SET calltype = 'Inbound'
WHERE calltype = 'in-bound';

UPDATE calldetails
SET callid = 'unknown'
WHERE callid = 'ageentsGradeLevel';

--data cleaning on calllog

UPDATE calllog
SET assignedto = agentid
WHERE assignedto is null;

SELECT * FROM calllog WHERE assignedto = agentid;
SELECT * FROM calllog WHERE assignedto is null;

UPDATE calllog
SET status = 'closed'
WHERE status ='CLOSED';

UPDATE calllog
SET status = 'pending'
WHERE status ='pEnding';

SELECT count(*),status FROM calllog GROUP BY status;

UPDATE calllog
SET resolutiondurationinhours = 'NA'
WHERE resolutiondurationinhours is null;

SELECT * FROM calllog WHERE resolutiondurationinhours is null;