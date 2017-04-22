CREATE SCHEMA quickandcleandb;

CREATE TABLE quickandcleandb.`user` ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	email                varchar(60)    ,
	username             varchar(60)    ,
	password_hash        varchar(128)    ,
	is_admin             bit    ,
	is_owner             bit    ,
	is_member            bit    ,
	is_authenticated     bit    ,
	is_anonymous         bit    ,
	is_active            bit    ,
	updated_at           int    ,
	created_at           int    ,
	locale               varchar(30)    ,
	timezone             varchar(60)    ,
	CONSTRAINT pk_user PRIMARY KEY ( id ),
	CONSTRAINT `ix_User_email` UNIQUE ( email ) ,
	CONSTRAINT `ix_User_username` UNIQUE ( username ) 
 );

CREATE INDEX ix_User_is_active ON quickandcleandb.`user` ( is_active );

CREATE INDEX ix_User_locale ON quickandcleandb.`user` ( locale );

CREATE INDEX ix_User_timezone ON quickandcleandb.`user` ( timezone );

CREATE TABLE quickandcleandb.asset ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	data_file_name       varchar(255)    ,
	data_content_type    varchar(255)    ,
	data_file_size       int    ,
	asset_type           varchar(30)    ,
	width                int    ,
	height               int    ,
	`description_en_US`  text    ,
	`description_fr_FR`  text    ,
	user_id              int    ,
	is_active            bit    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_asset PRIMARY KEY ( id ),
	CONSTRAINT asset_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX ix_Asset_asset_type ON quickandcleandb.asset ( asset_type );

CREATE INDEX ix_Asset_is_active ON quickandcleandb.asset ( is_active );

CREATE INDEX user_id ON quickandcleandb.asset ( user_id );

CREATE TABLE quickandcleandb.item ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	slug                 varchar(255)    ,
	`title_en_US`        varchar(255)    ,
	`title_fr_FR`        varchar(255)    ,
	`description_en_US`  text    ,
	`description_fr_FR`  text    ,
	amount               decimal(10,2)  NOT NULL  ,
	user_id              int    ,
	is_active            bit  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	`type`               varchar(255)    ,
	CONSTRAINT pk_item PRIMARY KEY ( id ),
	CONSTRAINT `ix_Item_slug` UNIQUE ( slug ) ,
	CONSTRAINT `ix_Item_title_en_US` UNIQUE ( `title_en_US` ) ,
	CONSTRAINT `ix_Item_title_fr_FR` UNIQUE ( `title_fr_FR` ) ,
	CONSTRAINT item_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX ix_Item_is_active ON quickandcleandb.item ( is_active );

CREATE INDEX user_id ON quickandcleandb.item ( user_id );

CREATE INDEX ix_Item_type ON quickandcleandb.item ( `type` );

CREATE TABLE quickandcleandb.`order` ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	status               varchar(30)    ,
	user_id              int    ,
	amount               decimal(10,2)  NOT NULL  ,
	is_active            bit    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_order PRIMARY KEY ( id ),
	CONSTRAINT order_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX ix_Order_is_active ON quickandcleandb.`order` ( is_active );

CREATE INDEX ix_Order_status ON quickandcleandb.`order` ( status );

CREATE INDEX user_id ON quickandcleandb.`order` ( user_id );

CREATE TABLE quickandcleandb.orderitem ( 
	order_id             int  NOT NULL  ,
	item_id              int  NOT NULL  ,
	options              text    ,
	unit_amount          decimal(10,2)  NOT NULL  ,
	quantity             int  NOT NULL  ,
	total_amount         decimal(10,2)  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_orderitem PRIMARY KEY ( order_id, item_id ),
	CONSTRAINT orderitem_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT orderitem_ibfk_1 FOREIGN KEY ( order_id ) REFERENCES quickandcleandb.`order`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX item_id ON quickandcleandb.orderitem ( item_id );

CREATE TABLE quickandcleandb.address ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	`type`               varchar(255)    ,
	`title_en_US`        varchar(255)    ,
	`title_fr_FR`        varchar(255)    ,
	address_line1        varchar(255)    ,
	address_line2        varchar(255)    ,
	city                 varchar(255)    ,
	postal_code          varchar(255)    ,
	state_region         varchar(255)    ,
	country              varchar(255)    ,
	full                 varchar(255)    ,
	time_zone            varchar(255)    ,
	latitude             decimal(9,6)  NOT NULL  ,
	longitude            decimal(9,6)  NOT NULL  ,
	amount               decimal(10,2)  NOT NULL  ,
	user_id              int    ,
	item_id              int    ,
	status               varchar(255)    ,
	is_active            bit  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_address PRIMARY KEY ( id ),
	CONSTRAINT `ix_Address_title_en_US` UNIQUE ( `title_en_US` ) ,
	CONSTRAINT `ix_Address_title_fr_FR` UNIQUE ( `title_fr_FR` ) ,
	CONSTRAINT address_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT address_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX item_id ON quickandcleandb.address ( item_id );

CREATE INDEX ix_Address_address_line1 ON quickandcleandb.address ( address_line1 );

CREATE INDEX ix_Address_address_line2 ON quickandcleandb.address ( address_line2 );

CREATE INDEX ix_Address_city ON quickandcleandb.address ( city );

CREATE INDEX ix_Address_country ON quickandcleandb.address ( country );

CREATE INDEX ix_Address_full ON quickandcleandb.address ( full );

CREATE INDEX ix_Address_is_active ON quickandcleandb.address ( is_active );

CREATE INDEX ix_Address_latitude ON quickandcleandb.address ( latitude );

CREATE INDEX ix_Address_longitude ON quickandcleandb.address ( longitude );

CREATE INDEX ix_Address_postal_code ON quickandcleandb.address ( postal_code );

CREATE INDEX ix_Address_state_region ON quickandcleandb.address ( state_region );

CREATE INDEX ix_Address_status ON quickandcleandb.address ( status );

CREATE INDEX ix_Address_time_zone ON quickandcleandb.address ( time_zone );

CREATE INDEX ix_Address_type ON quickandcleandb.address ( `type` );

CREATE INDEX user_id ON quickandcleandb.address ( user_id );

CREATE TABLE quickandcleandb.assetitem ( 
	asset_id             int  NOT NULL  ,
	item_id              int  NOT NULL  ,
	options              text    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_assetitem PRIMARY KEY ( asset_id, item_id ),
	CONSTRAINT assetitem_ibfk_1 FOREIGN KEY ( asset_id ) REFERENCES quickandcleandb.asset( id ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT assetitem_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX item_id ON quickandcleandb.assetitem ( item_id );

CREATE TABLE quickandcleandb.event ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	`type`               varchar(255)    ,
	`title_en_US`        varchar(255)    ,
	`title_fr_FR`        varchar(255)    ,
	amount               decimal(10,2)  NOT NULL  ,
	user_id              int    ,
	item_id              int    ,
	start                int    ,
	end                  int    ,
	days                 int    ,
	allday               bit    ,
	status               varchar(255)    ,
	is_active            bit  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	`description_en_US`  text    ,
	`description_fr_FR`  text    ,
	address_id           int    ,
	CONSTRAINT pk_event PRIMARY KEY ( id ),
	CONSTRAINT `ix_Event_title_en_US` UNIQUE ( `title_en_US` ) ,
	CONSTRAINT `ix_Event_title_fr_FR` UNIQUE ( `title_fr_FR` ) ,
	CONSTRAINT event_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT event_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT event_ibfk_3 FOREIGN KEY ( address_id ) REFERENCES quickandcleandb.address( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX item_id ON quickandcleandb.event ( item_id );

CREATE INDEX ix_Event_allday ON quickandcleandb.event ( allday );

CREATE INDEX ix_Event_days ON quickandcleandb.event ( days );

CREATE INDEX ix_Event_end ON quickandcleandb.event ( end );

CREATE INDEX ix_Event_is_active ON quickandcleandb.event ( is_active );

CREATE INDEX ix_Event_start ON quickandcleandb.event ( start );

CREATE INDEX ix_Event_status ON quickandcleandb.event ( status );

CREATE INDEX ix_Event_type ON quickandcleandb.event ( `type` );

CREATE INDEX user_id ON quickandcleandb.event ( user_id );

CREATE INDEX address_id ON quickandcleandb.event ( address_id );

CREATE TABLE quickandcleandb.useraddress ( 
	guest_id             int  NOT NULL  ,
	in_address_id        int  NOT NULL  ,
	options              text    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_useraddress PRIMARY KEY ( guest_id, in_address_id ),
	CONSTRAINT useraddress_ibfk_2 FOREIGN KEY ( in_address_id ) REFERENCES quickandcleandb.address( id ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT useraddress_ibfk_1 FOREIGN KEY ( guest_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX in_address_id ON quickandcleandb.useraddress ( in_address_id );

CREATE TABLE quickandcleandb.userevent ( 
	guest_id             int  NOT NULL  ,
	in_event_id          int  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	options              text    ,
	CONSTRAINT pk_userevent PRIMARY KEY ( guest_id, in_event_id ),
	CONSTRAINT userevent_ibfk_2 FOREIGN KEY ( in_event_id ) REFERENCES quickandcleandb.event( id ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT userevent_ibfk_1 FOREIGN KEY ( guest_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX in_event_id ON quickandcleandb.userevent ( in_event_id );

CREATE TABLE quickandcleandb.section ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	slug                 varchar(255)    ,
	parent_id            int    ,
	`title_en_US`        varchar(255)    ,
	`title_fr_FR`        varchar(255)    ,
	`description_en_US`  text    ,
	`description_fr_FR`  text    ,
	is_active            bit    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_section PRIMARY KEY ( id ),
	CONSTRAINT `ix_Section_slug` UNIQUE ( slug ) ,
	CONSTRAINT `ix_Section_title_en_US` UNIQUE ( `title_en_US` ) ,
	CONSTRAINT `ix_Section_title_fr_FR` UNIQUE ( `title_fr_FR` ) 
 );

CREATE INDEX ix_Section_is_active ON quickandcleandb.section ( is_active );

CREATE INDEX ix_Section_parent_id ON quickandcleandb.section ( parent_id );

CREATE TABLE quickandcleandb.sectionitem ( 
	section_id           int  NOT NULL  ,
	item_id              int  NOT NULL  ,
	options              text    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_sectionitem PRIMARY KEY ( section_id, item_id )
 );

CREATE INDEX item_id ON quickandcleandb.sectionitem ( item_id );

CREATE TABLE quickandcleandb.usersection ( 
	user_id              int  NOT NULL  ,
	section_id           int  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	options              text    ,
	CONSTRAINT pk_usersection PRIMARY KEY ( user_id, section_id )
 );

CREATE INDEX section_id ON quickandcleandb.usersection ( section_id );

ALTER TABLE quickandcleandb.section ADD CONSTRAINT section_ibfk_1 FOREIGN KEY ( parent_id ) REFERENCES quickandcleandb.section( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.sectionitem ADD CONSTRAINT sectionitem_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.sectionitem ADD CONSTRAINT sectionitem_ibfk_1 FOREIGN KEY ( section_id ) REFERENCES quickandcleandb.section( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.usersection ADD CONSTRAINT usersection_ibfk_2 FOREIGN KEY ( section_id ) REFERENCES quickandcleandb.section( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.usersection ADD CONSTRAINT usersection_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

