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
	CONSTRAINT pk_asset PRIMARY KEY ( id )
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
	price                decimal(10,2)  NOT NULL  ,
	user_id              int    ,
	is_active            bit  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_item PRIMARY KEY ( id ),
	CONSTRAINT `ix_Item_slug` UNIQUE ( slug ) ,
	CONSTRAINT `ix_Item_title_en_US` UNIQUE ( `title_en_US` ) ,
	CONSTRAINT `ix_Item_title_fr_FR` UNIQUE ( `title_fr_FR` ) 
 );

CREATE INDEX ix_Item_is_active ON quickandcleandb.item ( is_active );

CREATE INDEX user_id ON quickandcleandb.item ( user_id );

CREATE TABLE quickandcleandb.`order` ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	status               varchar(30)    ,
	user_id              int    ,
	amount               decimal(10,2)  NOT NULL  ,
	is_active            bit    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_order PRIMARY KEY ( id )
 );

CREATE INDEX ix_Order_is_active ON quickandcleandb.`order` ( is_active );

CREATE INDEX ix_Order_status ON quickandcleandb.`order` ( status );

CREATE INDEX user_id ON quickandcleandb.`order` ( user_id );

CREATE TABLE quickandcleandb.orderitem ( 
	order_id             int  NOT NULL  ,
	item_id              int  NOT NULL  ,
	options              text    ,
	unit_price           decimal(10,2)  NOT NULL  ,
	quantity             int  NOT NULL  ,
	total_price          decimal(10,2)  NOT NULL  ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_orderitem PRIMARY KEY ( order_id, item_id )
 );

CREATE INDEX item_id ON quickandcleandb.orderitem ( item_id );

CREATE TABLE quickandcleandb.assetitem ( 
	asset_id             int  NOT NULL  ,
	item_id              int  NOT NULL  ,
	options              text    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_assetitem PRIMARY KEY ( asset_id, item_id )
 );

CREATE INDEX item_id ON quickandcleandb.assetitem ( item_id );

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
	`description_en_US`  text    ,
	`description_fr_FR`  text    ,
	updated_at           int    ,
	created_at           int    ,
	CONSTRAINT pk_usersection PRIMARY KEY ( user_id, section_id )
 );

CREATE INDEX section_id ON quickandcleandb.usersection ( section_id );

ALTER TABLE quickandcleandb.asset ADD CONSTRAINT asset_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.assetitem ADD CONSTRAINT assetitem_ibfk_1 FOREIGN KEY ( asset_id ) REFERENCES quickandcleandb.asset( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.assetitem ADD CONSTRAINT assetitem_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.item ADD CONSTRAINT item_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.`order` ADD CONSTRAINT order_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.orderitem ADD CONSTRAINT orderitem_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.orderitem ADD CONSTRAINT orderitem_ibfk_1 FOREIGN KEY ( order_id ) REFERENCES quickandcleandb.`order`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.section ADD CONSTRAINT section_ibfk_1 FOREIGN KEY ( parent_id ) REFERENCES quickandcleandb.section( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.sectionitem ADD CONSTRAINT sectionitem_ibfk_2 FOREIGN KEY ( item_id ) REFERENCES quickandcleandb.item( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.sectionitem ADD CONSTRAINT sectionitem_ibfk_1 FOREIGN KEY ( section_id ) REFERENCES quickandcleandb.section( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.usersection ADD CONSTRAINT usersection_ibfk_2 FOREIGN KEY ( section_id ) REFERENCES quickandcleandb.section( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE quickandcleandb.usersection ADD CONSTRAINT usersection_ibfk_1 FOREIGN KEY ( user_id ) REFERENCES quickandcleandb.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

INSERT INTO quickandcleandb.`user`( id, email, username, password_hash, is_admin, is_owner, is_member, is_authenticated, is_anonymous, is_active, updated_at, created_at, locale, timezone ) VALUES ( 1, 'admin@example.com', 'admin@example.com', 'pbkdf2:sha1:1000$YOKWljpH$d2e8789a3ce4060778103f225314f14f0f985a7f', 1, 0, 1, 1, 0, 1, 1492357733, 1492293600, 'en_US', 'UTC' ); 
INSERT INTO quickandcleandb.`user`( id, email, username, password_hash, is_admin, is_owner, is_member, is_authenticated, is_anonymous, is_active, updated_at, created_at, locale, timezone ) VALUES ( 2, 'editor@example.com', 'editor@example.com', 'pbkdf2:sha1:1000$mipuQL9v$3871eb3f3ee8ad8a7d322f100cf09acc6a997aa0', 1, 0, 1, 1, 0, 1, 1492419023, 1492419023, 'en_US', 'UTC' ); 

INSERT INTO quickandcleandb.asset( id, data_file_name, data_content_type, data_file_size, asset_type, width, height, description_en_US, description_fr_FR, user_id, is_active, updated_at, created_at ) VALUES ( 1, 'avatar-systemaker-01.jpg', 'image/jpeg', 54370, 'image', 458, 458, 'description US', 'description FR', 1, 1, 1492470990, 1492293600 ); 
INSERT INTO quickandcleandb.asset( id, data_file_name, data_content_type, data_file_size, asset_type, width, height, description_en_US, description_fr_FR, user_id, is_active, updated_at, created_at ) VALUES ( 2, 'cheikhna2016.jpg', 'image/jpeg', 35966, 'image', 320, 320, 'description_en_US', 'description_fr_FR', 2, 1, 1492470990, 1492293600 ); 

INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, price, user_id, is_active, updated_at, created_at ) VALUES ( 1, 'product1', 'Product 1', 'Produit 1', 'description_en_US', 'description_fr_FR', 20.00, 1, 1, 1492456877, 1492293600 ); 
INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, price, user_id, is_active, updated_at, created_at ) VALUES ( 2, 'product2', 'Product2', 'Produit 2', 'description_en_US', 'description_fr_FR', 10.00, 2, 1, 1492470989, 1492293600 ); 
INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, price, user_id, is_active, updated_at, created_at ) VALUES ( 3, 'product3', 'product 3', 'produit 3', 'fdgdfgfdg', 'fdgdfgdfg', 10.00, 2, 1, 1492462741, 1492466400 ); 

INSERT INTO quickandcleandb.`order`( id, status, user_id, amount, is_active, updated_at, created_at ) VALUES ( 1, 'paid', 2, 30.00, 1, 1492470990, 1492466400 ); 
INSERT INTO quickandcleandb.`order`( id, status, user_id, amount, is_active, updated_at, created_at ) VALUES ( 2, 'pending', 1, 10.00, 1, 1492470990, 1492466400 ); 

INSERT INTO quickandcleandb.orderitem( order_id, item_id, options, unit_price, quantity, total_price, updated_at, created_at ) VALUES ( 1, 1, null, 20.00, 1, 20.00, 1492470989, 1492470989 ); 
INSERT INTO quickandcleandb.orderitem( order_id, item_id, options, unit_price, quantity, total_price, updated_at, created_at ) VALUES ( 1, 3, null, 10.00, 1, 10.00, 1492470989, 1492470989 ); 
INSERT INTO quickandcleandb.orderitem( order_id, item_id, options, unit_price, quantity, total_price, updated_at, created_at ) VALUES ( 2, 2, null, 10.00, 1, 10.00, 1492470989, 1492470989 ); 

INSERT INTO quickandcleandb.assetitem( asset_id, item_id, options, updated_at, created_at ) VALUES ( 1, 2, null, 1492357734, 1492357734 ); 
INSERT INTO quickandcleandb.assetitem( asset_id, item_id, options, updated_at, created_at ) VALUES ( 1, 3, null, 1492462741, 1492462741 ); 
INSERT INTO quickandcleandb.assetitem( asset_id, item_id, options, updated_at, created_at ) VALUES ( 2, 1, null, 1492462741, 1492462741 ); 
INSERT INTO quickandcleandb.assetitem( asset_id, item_id, options, updated_at, created_at ) VALUES ( 2, 2, null, 1492419023, 1492419023 ); 

INSERT INTO quickandcleandb.section( id, slug, parent_id, title_en_US, title_fr_FR, description_en_US, description_fr_FR, is_active, updated_at, created_at ) VALUES ( 1, 'global', null, 'Global', 'Globale', 'description_en_US', 'description_fr_FR', 1, 1492470989, 1492466400 ); 
INSERT INTO quickandcleandb.section( id, slug, parent_id, title_en_US, title_fr_FR, description_en_US, description_fr_FR, is_active, updated_at, created_at ) VALUES ( 2, 'section1', 1, 'Section 1', 'Section 1', 'description_en_US', 'description_fr_FR', 1, 1492470989, 1492466400 ); 
INSERT INTO quickandcleandb.section( id, slug, parent_id, title_en_US, title_fr_FR, description_en_US, description_fr_FR, is_active, updated_at, created_at ) VALUES ( 3, 'section2', 1, 'Section 2', 'Section 2', 'description_en_US', 'description_fr_FR', 1, 1492470989, 1492466400 ); 

INSERT INTO quickandcleandb.sectionitem( section_id, item_id, options, updated_at, created_at ) VALUES ( 1, 1, null, 1492466221, 1492466221 ); 
INSERT INTO quickandcleandb.sectionitem( section_id, item_id, options, updated_at, created_at ) VALUES ( 2, 2, null, 1492466221, 1492466221 ); 
INSERT INTO quickandcleandb.sectionitem( section_id, item_id, options, updated_at, created_at ) VALUES ( 3, 1, null, 1492470989, 1492470989 ); 
INSERT INTO quickandcleandb.sectionitem( section_id, item_id, options, updated_at, created_at ) VALUES ( 3, 3, null, 1492470989, 1492470989 ); 

INSERT INTO quickandcleandb.usersection( user_id, section_id, description_en_US, description_fr_FR, updated_at, created_at ) VALUES ( 1, 2, null, null, 1492466221, 1492466221 ); 
INSERT INTO quickandcleandb.usersection( user_id, section_id, description_en_US, description_fr_FR, updated_at, created_at ) VALUES ( 1, 3, null, null, 1492470989, 1492470989 ); 
INSERT INTO quickandcleandb.usersection( user_id, section_id, description_en_US, description_fr_FR, updated_at, created_at ) VALUES ( 2, 1, null, null, 1492466221, 1492466221 ); 

