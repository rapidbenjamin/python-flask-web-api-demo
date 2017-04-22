BEGIN TRANSACTION;
INSERT INTO `usersection` (user_id,section_id,options,updated_at,created_at) VALUES (1,1,NULL,1492636328,1492636328),
 (1,3,NULL,1492636328,1492636328),
 (2,1,NULL,1492636328,1492636328),
 (2,2,NULL,1492636328,1492636328);
INSERT INTO `userevent` (guest_id,in_event_id,options,updated_at,created_at) VALUES (1,1,NULL,1492564873,1492564873),
 (1,2,NULL,1492564873,1492564873),
 (1,3,NULL,1492565849,1492565849),
 (2,1,NULL,1492564873,1492564873),
 (2,3,NULL,1492565849,1492565849);
INSERT INTO `useraddress` (guest_id,in_address_id,options,updated_at,created_at) VALUES (1,1,NULL,1492891938,1492891938),
 (2,1,NULL,1492891938,1492891938),
 (1,2,NULL,1492893366,1492893366),
 (2,2,NULL,1492893366,1492893366);
INSERT INTO `sectionitem` (section_id,item_id,options,updated_at,created_at) VALUES (1,3,NULL,1492636328,1492636328),
 (2,1,NULL,1492636328,1492636328),
 (3,2,NULL,1492636328,1492636328),
 (3,3,NULL,1492636328,1492636328);
INSERT INTO `orderitem` (order_id,item_id,options,unit_amount,quantity,total_amount,updated_at,created_at) VALUES (1,2,NULL,0,1,0,1492472842,1492472842),
 (1,3,NULL,10,1,10,1492472842,1492472842),
 (2,1,NULL,20,1,20,1492472842,1492472842),
 (3,3,NULL,10,1,10,1492893945,1492893945);
INSERT INTO `assetitem` (asset_id,item_id,options,updated_at,created_at) VALUES (1,2,NULL,1492357734,1492357734),
 (1,3,NULL,1492462741,1492462741),
 (4,1,NULL,1492625364,1492625364);
INSERT INTO `User` (id,email,username,password_hash,is_admin,is_owner,is_member,is_authenticated,is_anonymous,is_active,updated_at,created_at,locale,timezone) VALUES (1,'admin@example.com','admin@example.com','pbkdf2:sha1:1000$YOKWljpH$d2e8789a3ce4060778103f225314f14f0f985a7f',1,0,1,1,0,1,1492357733,1492293600,'en_US','UTC'),
 (2,'editor@example.com','editor@example.com','pbkdf2:sha1:1000$mipuQL9v$3871eb3f3ee8ad8a7d322f100cf09acc6a997aa0',1,0,1,1,0,1,1492419023,1492419023,'en_US','UTC');
INSERT INTO `Section` (id,slug,parent_id,title_en_US,title_fr_FR,description_en_US,description_fr_FR,is_active,updated_at,created_at) VALUES (1,'global',NULL,'Global','Globale','description_en_US','description_fr_FR',1,1492471963,1492466400),
 (2,'section1',1,'Section 1','Section 1','description_en_US','description_fr_FR',1,1492471963,1492466400),
 (3,'section2',1,'Section 2','Section 2','description_en_US','description_fr_FR',1,1492471963,1492466400);
INSERT INTO `Order` (id,status,user_id,amount,is_active,updated_at,created_at) VALUES (1,'paid',2,10,1,1492472842,1492466400),
 (2,'pending',1,20,1,1492472842,1492466400),
 (3,'cart',1,10,1,1492893945,1492893945);
INSERT INTO `Item` (id,slug,type,title_en_US,title_fr_FR,description_en_US,description_fr_FR,amount,user_id,is_active,updated_at,created_at) VALUES (1,'product1','book','Product 1','Produit 1','<span style="color: #ff0000;"><em><strong>description_en_US</strong></em></span>','description_fr_FR',20,1,1,1492893945,1492293600),
 (2,'product2','cloth','Product2','Produit 2','description_en_US','description_fr_FR',0,2,1,1492893945,1492293600),
 (3,'product3','tool','product 3','produit 3','fdgdfgfdg','fdgdfgdfg',10,2,1,1492893945,1492466400);
INSERT INTO `Event` (id,type,title_en_US,title_fr_FR,description_en_US,description_fr_FR,amount,user_id,item_id,address_id,start,end,days,allday,status,is_active,updated_at,created_at) VALUES (1,'meeting','meeting 1','meeting 1','','',10,1,1,1,1492552800,1492639200,1,1,'pending',1,1492891938,1492564873),
 (2,'booking','booking 1','booking 1','','',100,2,3,1,1492552800,1492812000,3,1,'pending',1,1492891938,1492564873),
 (3,'lesson','lesson 1','cours 1','','',20,1,1,2,1492552800,1493416800,10,1,'pending',1,1492893946,1492565849);
INSERT INTO `Asset` (id,data_file_name,data_content_type,data_file_size,asset_type,width,height,description_en_US,description_fr_FR,user_id,is_active,updated_at,created_at) VALUES (1,'avatar-systemaker-01.jpg','image/jpeg',54370,'image',458,458,'description US','description FR',1,1,1492471963,1492293600),
 (3,'avatar-imagineer-01.jpg','image/jpeg',64188,'image',458,458,'','',NULL,1,1492472842,1492466400),
 (4,'test.txt','text/plain',7,'text',0,0,'','',1,1,1492627433,1492625364);
INSERT INTO `Address` (id,type,title_en_US,title_fr_FR,address_line1,address_line2,city,postal_code,state_region,country,full,time_zone,latitude,longitude,amount,user_id,item_id,status,is_active,updated_at,created_at) VALUES (1,'office','my office','mon bureau','5 Avenue Anatole France','','Paris','75007','Ile de france','France','5 Avenue Anatole France, Paris, 75007, Ile de france, France','2',48.86,2.29,20,1,1,'start',1,1492893366,1492891316),
 (2,'home','my home','ma maison','Champs-Élysées','','Paris','75008','Ile de france','France','Champs-Élysées, Paris, 75008, Ile de france, France','2',48.87,2.31,30,2,1,'start',1,1492893946,1492893366);
COMMIT;
