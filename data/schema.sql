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
INSERT INTO `usersection` (user_id,section_id,description_en_US,description_fr_FR,updated_at,created_at) VALUES (1,1,NULL,NULL,1491759772,1491759772);
CREATE TABLE "User" (
	id INTEGER NOT NULL, 
	email VARCHAR(60), 
	username VARCHAR(60), 
	password_hash VARCHAR(128), 
	asset_id INTEGER, 
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
	FOREIGN KEY(asset_id) REFERENCES "Asset" (id), 
	CHECK (is_admin IN (0, 1)), 
	CHECK (is_owner IN (0, 1)), 
	CHECK (is_member IN (0, 1)), 
	CHECK (is_authenticated IN (0, 1)), 
	CHECK (is_anonymous IN (0, 1)), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `User` (id,email,username,password_hash,asset_id,is_admin,is_owner,is_member,is_authenticated,is_anonymous,is_active,updated_at,created_at,locale,timezone) VALUES (1,'admin@example.com','admin','pbkdf2:sha1:1000$hSb7sGoA$ff10804b865b6691bdf813424dd213b3077a2cdc',1,1,0,1,1,0,1,1491759772,1491688800,'en_US','UTC');
CREATE TABLE "Section" (
	id INTEGER NOT NULL, 
	slug VARCHAR(255), 
	"title_en_US" VARCHAR(255), 
	"title_fr_FR" VARCHAR(255), 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `Section` (id,slug,title_en_US,title_fr_FR,description_en_US,description_fr_FR,is_active,updated_at,created_at) VALUES (1,'departmenta','Department A','Catégorie A','Section A','Section A',1,1491759772,1491688800);
CREATE TABLE "Asset" (
	id INTEGER NOT NULL, 
	assetable_id INTEGER, 
	assetable_type VARCHAR(30), 
	data_file_name VARCHAR(255), 
	data_content_type VARCHAR(255), 
	data_file_size INTEGER, 
	asset_type VARCHAR(30), 
	width INTEGER, 
	height INTEGER, 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	CHECK (is_active IN (0, 1))
);
INSERT INTO `Asset` (id,assetable_id,assetable_type,data_file_name,data_content_type,data_file_size,asset_type,width,height,description_en_US,description_fr_FR,is_active,updated_at,created_at) VALUES (1,'','','avatar-systemaker-01.jpg','image/jpeg',54370,'',458,458,'Avatar','Avatar',1,1491759772,1491688800);
CREATE INDEX "ix_usersection_description_fr_FR" ON usersection ("description_fr_FR");
CREATE INDEX "ix_usersection_description_en_US" ON usersection ("description_en_US");
CREATE UNIQUE INDEX "ix_User_username" ON "User" (username);
CREATE INDEX "ix_User_timezone" ON "User" (timezone);
CREATE INDEX "ix_User_locale" ON "User" (locale);
CREATE INDEX "ix_User_is_active" ON "User" (is_active);
CREATE UNIQUE INDEX "ix_User_email" ON "User" (email);
CREATE UNIQUE INDEX "ix_Section_title_fr_FR" ON "Section" ("title_fr_FR");
CREATE UNIQUE INDEX "ix_Section_title_en_US" ON "Section" ("title_en_US");
CREATE UNIQUE INDEX "ix_Section_slug" ON "Section" (slug);
CREATE INDEX "ix_Section_is_active" ON "Section" (is_active);
CREATE INDEX "ix_Section_description_fr_FR" ON "Section" ("description_fr_FR");
CREATE INDEX "ix_Section_description_en_US" ON "Section" ("description_en_US");
CREATE INDEX "ix_Asset_is_active" ON "Asset" (is_active);
CREATE INDEX "ix_Asset_assetable_type" ON "Asset" (assetable_type);
CREATE INDEX "ix_Asset_assetable_id" ON "Asset" (assetable_id);
CREATE INDEX "ix_Asset_asset_type" ON "Asset" (asset_type);
COMMIT;
