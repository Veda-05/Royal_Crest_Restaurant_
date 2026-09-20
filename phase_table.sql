CREATE TABLE SDLC (
  PHASE1 varchar(100),
  PHASE2 varchar(100),
  PHASE3 varchar(100),
  PHASE4 varchar(100),
  PHASE5 varchar(100),
  PHASE6 varchar(100)
);

INSERT INTO SDLC VALUES ('PLANNING & REQUIREMENT ANALYSIS','DEFINING REQUIREMENTS','DESIGN','DEVELOPMENT','TESTING','DEPLOYMENT & MAINTENANCE');
INSERT INTO SDLC VALUES ('Planning','defining','design','development','system testing','deployment and maintenance');
INSERT INTO SDLC VALUES ('define project scope','functional requirement','HLD','coding standard','manual testing','release planning');
INSERT INTO SDLC VALUES ('set objectives and goals','technical requirement','LLD','scalable code','automated testing','deployment automation');
INSERT INTO SDLC VALUES ('resource planning','requirement reviews and approved',' ','version control',' ','maintenance');
INSERT INTO SDLC VALUES (' ',' ',' ','code review',' ','feedbac');

SELECT * FROM SDLC ; 