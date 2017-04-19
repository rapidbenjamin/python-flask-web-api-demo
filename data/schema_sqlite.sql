
INSERT INTO `User` (id,email,username,password_hash,is_admin,is_owner,is_member,is_authenticated,is_anonymous,is_active,updated_at,created_at,locale,timezone) VALUES (1,'admin@example.com','admin@example.com','pbkdf2:sha1:1000$YOKWljpH$d2e8789a3ce4060778103f225314f14f0f985a7f',1,0,1,1,0,1,1492357733,1492293600,'en_US','UTC'),
 (2,'editor@example.com','editor@example.com','pbkdf2:sha1:1000$mipuQL9v$3871eb3f3ee8ad8a7d322f100cf09acc6a997aa0',1,0,1,1,0,1,1492419023,1492419023,'en_US','UTC');

INSERT INTO `Section` (id,slug,parent_id,title_en_US,title_fr_FR,description_en_US,description_fr_FR,is_active,updated_at,created_at) VALUES (1,'section1',3,'Section 1','Section 1','description_en_US','description_fr_FR',1,1492471963,1492466400),
 (2,'section2',3,'Section 2','Section 2','description_en_US','description_fr_FR',1,1492471963,1492466400),
 (3,'global',NULL,'Global','Globale','description_en_US','description_fr_FR',1,1492471963,1492466400);

INSERT INTO `Order` (id,status,user_id,amount,is_active,updated_at,created_at) VALUES (1,'paid',2,10,1,1492472842,1492466400),
 (2,'pending',1,20,1,1492472842,1492466400);

INSERT INTO `Item` (id,slug,title_en_US,title_fr_FR,description_en_US,description_fr_FR,amount,user_id,is_active,updated_at,created_at) VALUES (1,'product1','Product 1','Produit 1','description_en_US','description_fr_FR',20,1,1,1492456877,1492293600),
 (2,'product2','Product2','Produit 2','description_en_US','description_fr_FR',0,2,1,1492459454,1492293600),
 (3,'product3','product 3','produit 3','fdgdfgfdg','fdgdfgdfg',10,2,1,1492462741,1492466400);

INSERT INTO `Asset` (id,data_file_name,data_content_type,data_file_size,asset_type,width,height,description_en_US,description_fr_FR,user_id,is_active,updated_at,created_at) VALUES (1,'avatar-systemaker-01.jpg','image/jpeg',54370,'image',458,458,'description US','description FR',1,1,1492471963,1492293600),
 (3,'avatar-imagineer-01.jpg','image/jpeg',64188,'image',458,458,'','',NULL,1,1492472842,1492466400);

 
INSERT INTO `sectionitem` (section_id,item_id,options,updated_at,created_at) VALUES (1,1,NULL,1492466221,1492466221),
 (2,2,NULL,1492466221,1492466221),
 (3,1,NULL,1492471963,1492471963);

INSERT INTO `orderitem` (order_id,item_id,options,unit_amount,quantity,total_amount,updated_at,created_at) VALUES (1,2,NULL,0,1,0,1492472842,1492472842),
 (1,3,NULL,10,1,10,1492472842,1492472842),
 (2,1,NULL,20,1,20,1492472842,1492472842);

INSERT INTO `assetitem` (asset_id,item_id,options,updated_at,created_at) VALUES (1,2,NULL,1492357734,1492357734),
 (1,3,NULL,1492462741,1492462741);
