INSERT INTO quickandcleandb.`user`( id, email, username, password_hash, is_admin, is_owner, is_member, is_authenticated, is_anonymous, is_active, updated_at, created_at, locale, timezone ) VALUES ( 1, 'admin@example.com', 'admin@example.com', 'pbkdf2:sha1:1000$YOKWljpH$d2e8789a3ce4060778103f225314f14f0f985a7f', 1, 0, 1, 1, 0, 1, 1492357733, 1492293600, 'en_US', 'UTC' ); 
INSERT INTO quickandcleandb.`user`( id, email, username, password_hash, is_admin, is_owner, is_member, is_authenticated, is_anonymous, is_active, updated_at, created_at, locale, timezone ) VALUES ( 2, 'editor@example.com', 'editor@example.com', 'pbkdf2:sha1:1000$mipuQL9v$3871eb3f3ee8ad8a7d322f100cf09acc6a997aa0', 1, 0, 1, 1, 0, 1, 1492419023, 1492419023, 'en_US', 'UTC' ); 

INSERT INTO quickandcleandb.asset( id, data_file_name, data_content_type, data_file_size, asset_type, width, height, description_en_US, description_fr_FR, user_id, is_active, updated_at, created_at ) VALUES ( 1, 'avatar-systemaker-01.jpg', 'image/jpeg', 54370, 'image', 458, 458, 'description US', 'description FR', 1, 1, 1492471963, 1492293600 ); 
INSERT INTO quickandcleandb.asset( id, data_file_name, data_content_type, data_file_size, asset_type, width, height, description_en_US, description_fr_FR, user_id, is_active, updated_at, created_at ) VALUES ( 3, 'avatar-imagineer-01.jpg', 'image/jpeg', 64188, 'image', 458, 458, '', '', null, 1, 1492472842, 1492466400 ); 
INSERT INTO quickandcleandb.asset( id, data_file_name, data_content_type, data_file_size, asset_type, width, height, description_en_US, description_fr_FR, user_id, is_active, updated_at, created_at ) VALUES ( 4, 'test.txt', 'text/plain', 7, 'text', 0, 0, '', '', 1, 1, 1492627433, 1492625364 ); 

INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, amount, user_id, is_active, updated_at, created_at ) VALUES ( 1, 'product1', 'Product 1', 'Produit 1', 'description_en_US', 'description_fr_FR', 20.00, 1, 1, 1492456877, 1492293600 ); 
INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, amount, user_id, is_active, updated_at, created_at ) VALUES ( 2, 'product2', 'Product2', 'Produit 2', 'description_en_US', 'description_fr_FR', 0.00, 2, 1, 1492459454, 1492293600 ); 
INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, amount, user_id, is_active, updated_at, created_at ) VALUES ( 3, 'product3', 'product 3', 'produit 3', 'fdgdfgfdg', 'fdgdfgdfg', 10.00, 2, 1, 1492462741, 1492466400 ); 

INSERT INTO quickandcleandb.`order`( id, status, user_id, amount, is_active, updated_at, created_at ) VALUES ( 1, 'paid', 2, 10.00, 1, 1492472842, 1492466400 ); 
INSERT INTO quickandcleandb.`order`( id, status, user_id, amount, is_active, updated_at, created_at ) VALUES ( 2, 'pending', 1, 20.00, 1, 1492472842, 1492466400 ); 

INSERT INTO quickandcleandb.orderitem( order_id, item_id, options, unit_amount, quantity, total_amount, updated_at, created_at ) VALUES ( 1, 2, null, 0.00, 1, 0.00, 1492472842, 1492472842 ); 
INSERT INTO quickandcleandb.orderitem( order_id, item_id, options, unit_amount, quantity, total_amount, updated_at, created_at ) VALUES ( 1, 3, null, 10.00, 1, 10.00, 1492472842, 1492472842 ); 
INSERT INTO quickandcleandb.orderitem( order_id, item_id, options, unit_amount, quantity, total_amount, updated_at, created_at ) VALUES ( 2, 1, null, 20.00, 1, 20.00, 1492472842, 1492472842 ); 

INSERT INTO quickandcleandb.assetitem( asset_id, item_id, options, updated_at, created_at ) VALUES ( 1, 2, null, 1492357734, 1492357734 ); 
INSERT INTO quickandcleandb.assetitem( asset_id, item_id, options, updated_at, created_at ) VALUES ( 1, 3, null, 1492462741, 1492462741 ); 
INSERT INTO quickandcleandb.assetitem( asset_id, item_id, options, updated_at, created_at ) VALUES ( 4, 1, null, 1492625364, 1492625364 ); 

INSERT INTO quickandcleandb.event( id, type, title_en_US, title_fr_FR, amount, user_id, item_id, start, end, days, allday, status, is_active, updated_at, created_at ) VALUES ( 1, 'meeting', 'meeting 1', 'meeting 1', 10.00, 1, 1, 1492552800, 1492639200, 1, 1, 'pending', 1, 1492565582, 1492564873 ); 
INSERT INTO quickandcleandb.event( id, type, title_en_US, title_fr_FR, amount, user_id, item_id, start, end, days, allday, status, is_active, updated_at, created_at ) VALUES ( 2, 'booking', 'booking 1', 'booking 1', 100.00, 2, 3, 1492552800, 1492812000, 3, 1, 'pending', 1, 1492565582, 1492564873 ); 
INSERT INTO quickandcleandb.event( id, type, title_en_US, title_fr_FR, amount, user_id, item_id, start, end, days, allday, status, is_active, updated_at, created_at ) VALUES ( 3, 'lesson', 'lesson 1', 'cours 1', 20.00, 1, 2, 1492552800, 1493416800, 10, 1, 'pending', 1, 1492565849, 1492565849 ); 

INSERT INTO quickandcleandb.userevent( guest_id, in_event_id, options, updated_at, created_at ) VALUES ( 1, 1, null, 1492564873, 1492564873 ); 
INSERT INTO quickandcleandb.userevent( guest_id, in_event_id, options, updated_at, created_at ) VALUES ( 1, 2, null, 1492564873, 1492564873 ); 
INSERT INTO quickandcleandb.userevent( guest_id, in_event_id, options, updated_at, created_at ) VALUES ( 1, 3, null, 1492565849, 1492565849 ); 
INSERT INTO quickandcleandb.userevent( guest_id, in_event_id, options, updated_at, created_at ) VALUES ( 2, 1, null, 1492564873, 1492564873 ); 
INSERT INTO quickandcleandb.userevent( guest_id, in_event_id, options, updated_at, created_at ) VALUES ( 2, 3, null, 1492565849, 1492565849 ); 

INSERT INTO quickandcleandb.section( id, slug, parent_id, title_en_US, title_fr_FR, description_en_US, description_fr_FR, is_active, updated_at, created_at ) VALUES ( 1, 'global', null, 'Global', 'Globale', 'description_en_US', 'description_fr_FR', 1, 1492471963, 1492466400 ); 
INSERT INTO quickandcleandb.section( id, slug, parent_id, title_en_US, title_fr_FR, description_en_US, description_fr_FR, is_active, updated_at, created_at ) VALUES ( 2, 'section1', 1, 'Section 1', 'Section 1', 'description_en_US', 'description_fr_FR', 1, 1492471963, 1492466400 ); 
INSERT INTO quickandcleandb.section( id, slug, parent_id, title_en_US, title_fr_FR, description_en_US, description_fr_FR, is_active, updated_at, created_at ) VALUES ( 3, 'section2', 1, 'Section 2', 'Section 2', 'description_en_US', 'description_fr_FR', 1, 1492471963, 1492466400 ); 

