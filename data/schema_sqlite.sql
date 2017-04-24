BEGIN TRANSACTION;
CREATE TABLE usersection (
	user_id INTEGER NOT NULL, 
	section_id INTEGER NOT NULL, 
	options TEXT, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (user_id, section_id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	FOREIGN KEY(section_id) REFERENCES "Section" (id)
);
CREATE TABLE userevent (
	guest_id INTEGER NOT NULL, 
	in_event_id INTEGER NOT NULL, 
	options TEXT, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (guest_id, in_event_id), 
	FOREIGN KEY(guest_id) REFERENCES "User" (id), 
	FOREIGN KEY(in_event_id) REFERENCES "Event" (id)
);
CREATE TABLE useraddress (
	guest_id INTEGER NOT NULL, 
	in_address_id INTEGER NOT NULL, 
	options TEXT, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (guest_id, in_address_id), 
	FOREIGN KEY(guest_id) REFERENCES "User" (id), 
	FOREIGN KEY(in_address_id) REFERENCES "Address" (id)
);
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
CREATE TABLE orderitem (
	order_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	options TEXT, 
	unit_amount NUMERIC(10, 2) NOT NULL, 
	quantity INTEGER NOT NULL, 
	total_amount NUMERIC(10, 2) NOT NULL, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (order_id, item_id), 
	FOREIGN KEY(order_id) REFERENCES "Order" (id), 
	FOREIGN KEY(item_id) REFERENCES "Item" (id)
);
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
CREATE TABLE "User" (
	id INTEGER NOT NULL, 
	email VARCHAR(60), 
	username VARCHAR(60), 
	password_hash VARCHAR(128), 
	first_name VARCHAR(128), 
	last_name VARCHAR(128), 
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
CREATE TABLE "Payment" (
	id INTEGER NOT NULL, 
	status VARCHAR(30), 
	key_id VARCHAR(255), 
	user_id INTEGER, 
	order_id INTEGER, 
	creditcard_id INTEGER, 
	ip_address VARCHAR(255), 
	intent VARCHAR(255), 
	return_url VARCHAR(255), 
	cancel_url VARCHAR(255), 
	payment_method VARCHAR(255), 
	amount NUMERIC(10, 2) NOT NULL, 
	currency VARCHAR(255), 
	params TEXT, 
	comments TEXT, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	FOREIGN KEY(order_id) REFERENCES "Order" (id), 
	FOREIGN KEY(creditcard_id) REFERENCES "Creditcard" (id), 
	CHECK (is_active IN (0, 1))
);
CREATE TABLE "Order" (
	id INTEGER NOT NULL, 
	status VARCHAR(30), 
	user_id INTEGER, 
	amount NUMERIC(10, 2) NOT NULL, 
	params TEXT, 
	comments TEXT, 
	is_active BOOLEAN, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	CHECK (is_active IN (0, 1))
);
CREATE TABLE "Item" (
	id INTEGER NOT NULL, 
	slug VARCHAR(255), 
	type VARCHAR(255), 
	"title_en_US" VARCHAR(255), 
	"title_fr_FR" VARCHAR(255), 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	amount NUMERIC(10, 2) NOT NULL, 
	user_id INTEGER, 
	is_active BOOLEAN NOT NULL, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	CHECK (is_active IN (0, 1))
);
CREATE TABLE "Event" (
	id INTEGER NOT NULL, 
	type VARCHAR(255), 
	"title_en_US" VARCHAR(255), 
	"title_fr_FR" VARCHAR(255), 
	"description_en_US" TEXT, 
	"description_fr_FR" TEXT, 
	amount NUMERIC(10, 2) NOT NULL, 
	user_id INTEGER, 
	item_id INTEGER, 
	address_id INTEGER, 
	start INTEGER, 
	"end" INTEGER, 
	days INTEGER, 
	allday BOOLEAN, 
	status VARCHAR(255), 
	is_active BOOLEAN NOT NULL, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	FOREIGN KEY(item_id) REFERENCES "Item" (id), 
	FOREIGN KEY(address_id) REFERENCES "Address" (id), 
	CHECK (allday IN (0, 1)), 
	CHECK (is_active IN (0, 1))
);
CREATE TABLE "Creditcard" (
	`id`	INTEGER NOT NULL,
	`status`	VARCHAR(30),
	`key_id`	VARCHAR(255),
	`user_id`	INTEGER,
	`type`	VARCHAR(255),
	`encrypted_number`	TEXT,
	`expire_month`	INTEGER,
	`expire_year`	INTEGER,
	`first_name`	VARCHAR(255),
	`last_name`	VARCHAR(255),
	`params`	TEXT,
	`comments`	TEXT,
	`is_active`	BOOLEAN,
	`updated_at`	INTEGER,
	`created_at`	INTEGER,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`user_id`) REFERENCES `User`(`id`)
);
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
CREATE TABLE "Address" (
	id INTEGER NOT NULL, 
	type VARCHAR(255), 
	"title_en_US" VARCHAR(255), 
	"title_fr_FR" VARCHAR(255), 
	address_line1 VARCHAR(255), 
	address_line2 VARCHAR(255), 
	city VARCHAR(255), 
	postal_code VARCHAR(255), 
	state_region VARCHAR(255), 
	country VARCHAR(255), 
	country_code VARCHAR(255), 
	"full" VARCHAR(255), 
	time_zone VARCHAR(255), 
	latitude NUMERIC(9, 6) NOT NULL, 
	longitude NUMERIC(9, 6) NOT NULL, 
	amount NUMERIC(10, 2) NOT NULL, 
	user_id INTEGER, 
	item_id INTEGER, 
	status VARCHAR(255), 
	is_active BOOLEAN NOT NULL, 
	updated_at INTEGER, 
	created_at INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id), 
	FOREIGN KEY(item_id) REFERENCES "Item" (id), 
	CHECK (is_active IN (0, 1))
);
CREATE UNIQUE INDEX "ix_User_username" ON "User" (username);
CREATE INDEX "ix_User_timezone" ON "User" (timezone);
CREATE INDEX "ix_User_locale" ON "User" (locale);
CREATE INDEX "ix_User_last_name" ON "User" (last_name);
CREATE INDEX "ix_User_is_active" ON "User" (is_active);
CREATE INDEX "ix_User_first_name" ON "User" (first_name);
CREATE UNIQUE INDEX "ix_User_email" ON "User" (email);
CREATE UNIQUE INDEX "ix_Section_title_fr_FR" ON "Section" ("title_fr_FR");
CREATE UNIQUE INDEX "ix_Section_title_en_US" ON "Section" ("title_en_US");
CREATE UNIQUE INDEX "ix_Section_slug" ON "Section" (slug);
CREATE INDEX "ix_Section_parent_id" ON "Section" (parent_id);
CREATE INDEX "ix_Section_is_active" ON "Section" (is_active);
CREATE INDEX "ix_Payment_status" ON "Payment" (status);
CREATE INDEX "ix_Payment_key_id" ON "Payment" (key_id);
CREATE INDEX "ix_Payment_is_active" ON "Payment" (is_active);
CREATE INDEX "ix_Order_status" ON "Order" (status);
CREATE INDEX "ix_Order_is_active" ON "Order" (is_active);
CREATE INDEX "ix_Item_type" ON "Item" (type);
CREATE UNIQUE INDEX "ix_Item_title_fr_FR" ON "Item" ("title_fr_FR");
CREATE UNIQUE INDEX "ix_Item_title_en_US" ON "Item" ("title_en_US");
CREATE UNIQUE INDEX "ix_Item_slug" ON "Item" (slug);
CREATE INDEX "ix_Item_is_active" ON "Item" (is_active);
CREATE INDEX "ix_Event_type" ON "Event" (type);
CREATE UNIQUE INDEX "ix_Event_title_fr_FR" ON "Event" ("title_fr_FR");
CREATE UNIQUE INDEX "ix_Event_title_en_US" ON "Event" ("title_en_US");
CREATE INDEX "ix_Event_status" ON "Event" (status);
CREATE INDEX "ix_Event_start" ON "Event" (start);
CREATE INDEX "ix_Event_is_active" ON "Event" (is_active);
CREATE INDEX "ix_Event_end" ON "Event" ("end");
CREATE INDEX "ix_Event_days" ON "Event" (days);
CREATE INDEX "ix_Event_allday" ON "Event" (allday);
CREATE INDEX "ix_Asset_is_active" ON "Asset" (is_active);
CREATE INDEX "ix_Asset_asset_type" ON "Asset" (asset_type);
CREATE INDEX "ix_Address_type" ON "Address" (type);
CREATE UNIQUE INDEX "ix_Address_title_fr_FR" ON "Address" ("title_fr_FR");
CREATE UNIQUE INDEX "ix_Address_title_en_US" ON "Address" ("title_en_US");
CREATE INDEX "ix_Address_time_zone" ON "Address" (time_zone);
CREATE INDEX "ix_Address_status" ON "Address" (status);
CREATE INDEX "ix_Address_state_region" ON "Address" (state_region);
CREATE INDEX "ix_Address_postal_code" ON "Address" (postal_code);
CREATE INDEX "ix_Address_longitude" ON "Address" (longitude);
CREATE INDEX "ix_Address_latitude" ON "Address" (latitude);
CREATE INDEX "ix_Address_is_active" ON "Address" (is_active);
CREATE INDEX "ix_Address_full" ON "Address" ("full");
CREATE INDEX "ix_Address_country_code" ON "Address" (country_code);
CREATE INDEX "ix_Address_country" ON "Address" (country);
CREATE INDEX "ix_Address_city" ON "Address" (city);
CREATE INDEX "ix_Address_address_line2" ON "Address" (address_line2);
CREATE INDEX "ix_Address_address_line1" ON "Address" (address_line1);
COMMIT;
