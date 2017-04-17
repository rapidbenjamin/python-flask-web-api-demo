
INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, price, is_active, updated_at, created_at ) VALUES ( 1, 'product1', 'Product 1', 'Produit 1', 'description_en_US', 'description_fr_FR', 0.0,  1, 1492357734, 1492293600 ); 
INSERT INTO quickandcleandb.item( id, slug, title_en_US, title_fr_FR, description_en_US, description_fr_FR, price, is_active, updated_at, created_at ) VALUES ( 2, 'product2', 'Product2', 'Produit 2', 'description_en_US', 'description_fr_FR', 0.0, 1, 1492357734, 1492293600 ); 

INSERT INTO quickandcleandb.`user`( id, email, username, password_hash, is_admin, is_owner, is_member, is_authenticated, is_anonymous, is_active, updated_at, created_at, locale, timezone ) VALUES ( 1, 'admin@example.com', 'admin@example.com', 'pbkdf2:sha1:1000$YOKWljpH$d2e8789a3ce4060778103f225314f14f0f985a7f', 1, 0, 1, 1, 0, 1, 1492357733, 1492293600, 'en_US', 'UTC' ); 
INSERT INTO quickandcleandb.`user`( id, email, username, password_hash, is_admin, is_owner, is_member, is_authenticated, is_anonymous, is_active, updated_at, created_at, locale, timezone ) VALUES ( 2, 'editor@example.com', 'editor@example.com', 'pbkdf2:sha1:1000$mipuQL9v$3871eb3f3ee8ad8a7d322f100cf09acc6a997aa0', 1, 0, 1, 1, 0, 1, 1492419023, 1492419023, 'en_US', 'UTC' ); 

INSERT INTO quickandcleandb.asset( id, data_file_name, data_content_type, data_file_size, asset_type, width, height, description_en_US, description_fr_FR, user_id, is_active, updated_at, created_at ) VALUES ( 1, 'avatar-systemaker-01.jpg', 'image/jpeg', 54370, '', 458, 458, 'description US', 'description FR', 1, 1, 1492357235, 1492293600 ); 
INSERT INTO quickandcleandb.asset( id, data_file_name, data_content_type, data_file_size, asset_type, width, height, description_en_US, description_fr_FR, user_id, is_active, updated_at, created_at ) VALUES ( 2, 'cheikhna2016.jpg', 'image/jpeg', 35966, '', 320, 320, 'description_en_US', 'description_fr_FR', 2, 1, 1492419023, 1492293600 ); 

INSERT INTO quickandcleandb.assetitem( asset_id, item_id, updated_at, created_at ) VALUES ( 1, 1, 1492357734, 1492357734 ); 
INSERT INTO quickandcleandb.assetitem( asset_id, item_id, updated_at, created_at ) VALUES ( 1, 2, 1492357734, 1492357734 ); 
INSERT INTO quickandcleandb.assetitem( asset_id, item_id, updated_at, created_at ) VALUES ( 2, 2, 1492419023, 1492419023 ); 

