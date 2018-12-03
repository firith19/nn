select * from dokument;

SET SQL_SAFE_UPDATES = 0;
delete from dokument;
ALTER TABLE dokument AUTO_INCREMENT = 1;
SET SQL_SAFE_UPDATES = 1;

select * from dokument_dokument;



