create table dokument
(
id int not null auto_increment,
nn_id int not null,
oznaka_broj varchar(32),
naziv varchar(200),
vrsta_dokumenta varchar(200),
vrsta_ugovora varchar(200),
cpv varchar(200),
vrsta_postupka varchar(200),
rok_za_dostavu_ponuda datetime,
datum_objave datetime,
datum_slanja datetime,
zakon varchar(200),
ime_dokumenta varchar(200)
PRIMARY KEY (ID)
);

create table dokument_dokument
(
id int not null auto_increment,
dokument1_id int,
dokument2_id int,
PRIMARY KEY (ID),
foreign key (dokument1_id) references dokument(id),
foreign key (dokument2_id) references dokument(id)
);

create table firma
(
id int not null auto_increment,
oib varchar(16),
PRIMARY KEY (ID)
);

create table dokument_firma
(
id int not null auto_increment,
dokument_id int,
firma_id int,
PRIMARY KEY (ID),
foreign key (dokument_id) references dokument(id),
foreign key (firma_id) references firma(id)
);

create table ponuda
(
id int not null auto_increment,
firma_id int,
iznos float,
dobila boolean,
PRIMARY KEY (ID)
);

create table dokument_ponuda
(
id int not null auto_increment,
dokument_id int,
ponuda_id int,
PRIMARY KEY (ID),
foreign key (dokument_id) references dokument(id),
foreign key (ponuda_id) references ponuda(id)
);

create table dokument_download
(
nn_id int not null,
ime_dokumenta varchar(200),
PRIMARY KEY (nn_id)
);

create table log
(
id int not null auto_increment,
msg varchar(200),
log_level varchar(8),
PRIMARY KEY (ID)
);
