BEGIN TRANSACTION;
CREATE TABLE usersection (
	user_id INTEGER NOT NULL, 
	section_id INTEGER NOT NULL, 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (user_id, section_id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	FOREIGN KEY(section_id) REFERENCES "Section" (id)
);
INSERT INTO `usersection` (user_id,section_id,description_en_US,description_fr_FR,updated_at,created_at) VALUES (2,1,NULL,NULL,1492466221,1492466221),
 (1,2,NULL,NULL,1492466221,1492466221),
 (1,3,NULL,NULL,1492471963,1492471963);
CREATE TABLE sectionitem (
	section_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	options TEXT, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (section_id, item_id), 
	FOREIGN KEY(section_id) REFERENCES "Section" (id), 
	FOREIGN KEY(item_id) REFERENCES "Item" (id)
);
INSERT INTO `sectionitem` (section_id,item_id,options,updated_at,created_at) VALUES (1,1,NULL,1492466221,1492466221),
 (2,2,NULL,1492466221,1492466221),
 (3,1,NULL,1492471963,1492471963);
CREATE TABLE orderitem (
	order_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	options TEXT, 
	unit_price NUMERIC(10, 2) NOT NULL, 
	quantity INTEGER NOT NULL, 
	total_price NUMERIC(10, 2) NOT NULL, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (order_id, item_id), 
	FOREIGN KEY(order_id) REFERENCES "Order" (id), 
	FOREIGN KEY(item_id) REFERENCES "Item" (id)
);
INSERT INTO `orderitem` (order_id,item_id,options,unit_price,quantity,total_price,updated_at,created_at) VALUES (1,2,NULL,0,1,0,1492472842,1492472842),
 (1,3,NULL,10,1,10,1492472842,1492472842),
 (2,1,NULL,20,1,20,1492472842,1492472842);
CREATE TABLE assetitem (
	asset_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	options TEXT, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (asset_id, item_id), 
	FOREIGN KEY(asset_id) REFERENCES "Asset" (id), 
	FOREIGN KEY(item_id) REFERENCES "Item" (id)
);
INSERT INTO `assetitem` (asset_id,item_id,options,updated_at,created_at) VALUES (1,2,NULL,1492357734,1492357734),
 (1,3,NULL,1492462741,1492462741);
CREATE TABLE "User" (
	id INTEGER NOT NULL, 
	email VARCHAR(60), 
	username VARCHAR(60), 
	password_hash VARCHAR(128), 
	is_admin BOOLEAN, 
	is_owner BOOLEAN, 
	is_member BOOLEAN, 
	is_authenticated BOOLEAN, 
	is_anonymous BOOLEAN, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	locale VARCHAR(30), 
	timezone VARCHAR(60), 
	PRIMARY KEY (id), 
	CHECK (is_admin IN (0, 1)), 
	CHECK (is_owner IN (0, 1)), 
	CHECK (is_member IN (0, 1)), 
	CHECK (is_authenticated IN (0, 1)), 
	CHECK (is_anonymous IN (0, 1)), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `User` (id,email,username,password_hash,is_admin,is_owner,is_member,is_authenticated,is_anonymous,is_active,updated_at,created_at,locale,timezone) VALUES (1,'admin@example.com','admin@example.com','pbkdf2:sha1:1000$YOKWljpH$d2e8789a3ce4060778103f225314f14f0f985a7f',1,0,1,1,0,1,1492357733,1492293600,'en_US','UTC'),
 (2,'editor@example.com','editor@example.com','pbkdf2:sha1:1000$mipuQL9v$3871eb3f3ee8ad8a7d322f100cf09acc6a997aa0',1,0,1,1,0,1,1492419023,1492419023,'en_US','UTC');
CREATE TABLE "Section" (
	id INTEGER NOT NULL, 
	slug VARCHAR(255), 
	parent_id INTEGER, 
	"title_en_US" VARCHAR(255), 
	"title_fr_FR" VARCHAR(255), 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES "Section" (id), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `Section` (id,slug,parent_id,title_en_US,title_fr_FR,description_en_US,description_fr_FR,is_active,updated_at,created_at) VALUES (1,'section1',3,'Section 1','Section 1','description_en_US','description_fr_FR',1,1492471963,1492466400),
 (2,'section2',3,'Section 2','Section 2','description_en_US','description_fr_FR',1,1492471963,1492466400),
 (3,'global',NULL,'Global','Globale','description_en_US','description_fr_FR',1,1492471963,1492466400);
CREATE TABLE "Order" (
	id INTEGER NOT NULL, 
	status VARCHAR(30), 
	user_id INTEGER, 
	amount NUMERIC(10, 2) NOT NULL, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `Order` (id,status,user_id,amount,is_active,updated_at,created_at) VALUES (1,'paid',2,10,1,1492472842,1492466400),
 (2,'pending',1,20,1,1492472842,1492466400);
CREATE TABLE "Item" (
	id INTEGER NOT NULL, 
	slug VARCHAR(255), 
	"title_en_US" VARCHAR(255), 
	"title_fr_FR" VARCHAR(255), 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	price NUMERIC(10, 2) NOT NULL, 
	user_id INTEGER, 
	is_active BOOLEAN NOT NULL, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `Item` (id,slug,title_en_US,title_fr_FR,description_en_US,description_fr_FR,price,user_id,is_active,updated_at,created_at) VALUES (1,'product1','Product 1','Produit 1','description_en_US','description_fr_FR',20,1,1,1492456877,1492293600),
 (2,'product2','Product2','Produit 2','description_en_US','description_fr_FR',0,2,1,1492459454,1492293600),
 (3,'product3','product 3','produit 3','fdgdfgfdg','fdgdfgdfg',10,2,1,1492462741,1492466400);
CREATE TABLE "Asset" (
	id INTEGER NOT NULL, 
	data_file_name VARCHAR(255), 
	data_content_type VARCHAR(255), 
	data_file_size INTEGER, 
	asset_type VARCHAR(30), 
	width INTEGER, 
	height INTEGER, 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	user_id INTEGER, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `Asset` (id,data_file_name,data_content_type,data_file_size,asset_type,width,height,description_en_US,description_fr_FR,user_id,is_active,updated_at,created_at) VALUES (1,'avatar-systemaker-01.jpg','image/jpeg',54370,'image',458,458,'description US','description FR',1,1,1492471963,1492293600),
 (3,'avatar-imagineer-01.jpg','image/jpeg',64188,'image',458,458,'','',NULL,1,1492472842,1492466400);
CREATE UNIQUE INDEX "ix_User_username" ON "User" (username);
CREATE INDEX "ix_User_timezone" ON "User" (timezone);
CREATE INDEX "ix_User_locale" ON "User" (locale);
CREATE INDEX "ix_User_is_active" ON "User" (is_active);
CREATE UNIQUE INDEX "ix_User_email" ON "User" (email);
CREATE UNIQUE INDEX "ix_Section_title_fr_FR" ON "Section" ("title_fr_FR");
CREATE UNIQUE INDEX "ix_Section_title_en_US" ON "Section" ("title_en_US");
CREATE UNIQUE INDEX "ix_Section_slug" ON "Section" (slug);
CREATE INDEX "ix_Section_parent_id" ON "Section" (parent_id);
CREATE INDEX "ix_Section_is_active" ON "Section" (is_active);
CREATE INDEX "ix_Order_status" ON "Order" (status);
CREATE INDEX "ix_Order_is_active" ON "Order" (is_active);
CREATE UNIQUE INDEX "ix_Item_title_fr_FR" ON "Item" ("title_fr_FR");
CREATE UNIQUE INDEX "ix_Item_title_en_US" ON "Item" ("title_en_US");
CREATE UNIQUE INDEX "ix_Item_slug" ON "Item" (slug);
CREATE INDEX "ix_Item_is_active" ON "Item" (is_active);
CREATE INDEX "ix_Asset_is_active" ON "Asset" (is_active);
CREATE INDEX "ix_Asset_asset_type" ON "Asset" (asset_type);
COMMIT;
