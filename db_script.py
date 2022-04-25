import mysql.connector
import logging

HOST = '206.189.138.203'

log_file = 'db_log.log'
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.FileHandler(log_file)
handler.setFormatter(formatter)
logger = logging.getLogger('db_log')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def conn_db(db_name):
    mydb = mysql.connector.connect(
            host = HOST,
            user = "remote",
            password = "password",
            database = db_name)
    return mydb

def create_user(user, password, cursor):
    cursor.execute("CREATE USER'{}'@'%' IDENTIFIED BY '{}';".format(user, password))
    cursor.execute("FLUSH PRIVILEGES;")

def create_db(dbname, cursor):
    cursor.execute("CREATE DATABASE {};".format(dbname))

def create_tables_and_add_user(dbname, admin, admin_pass, cursor):
    cursor.execute('''CREATE TABLE wp_commentmeta (
        meta_id bigint(20) unsigned NOT NULL auto_increment,
        comment_id bigint(20) unsigned NOT NULL default '0',
        meta_key varchar(255) default NULL,
        meta_value longtext,
        PRIMARY KEY  (meta_id),
        KEY comment_id (comment_id),
        KEY meta_key (meta_key));
    ''')

    cursor.execute('''CREATE TABLE wp_comments (
        comment_ID bigint(20) unsigned NOT NULL auto_increment,
        comment_post_ID bigint(20) unsigned NOT NULL default '0',
        comment_author tinytext NOT NULL,
        comment_author_email varchar(100) NOT NULL default '',
        comment_author_url varchar(200) NOT NULL default '',
        comment_author_IP varchar(100) NOT NULL default '',
        comment_date datetime NOT NULL default '0000-00-00 00:00:00',
        comment_date_gmt datetime NOT NULL default '0000-00-00 00:00:00',
        comment_content text NOT NULL,
        comment_karma int(11) NOT NULL default '0',
        comment_approved varchar(20) NOT NULL default '1',
        comment_agent varchar(255) NOT NULL default '',
        comment_type varchar(20) NOT NULL default 'comment',
        comment_parent bigint(20) unsigned NOT NULL default '0',
        user_id bigint(20) unsigned NOT NULL default '0',
        PRIMARY KEY  (comment_ID),
        KEY comment_post_ID (comment_post_ID),
        KEY comment_approved_date_gmt (comment_approved,comment_date_gmt),
        KEY comment_date_gmt (comment_date_gmt),
        KEY comment_parent (comment_parent),
        KEY comment_author_email (comment_author_email(10)));
    ''')

    cursor.execute('''CREATE TABLE wp_links (
        link_id bigint(20) unsigned NOT NULL auto_increment,
        link_url varchar(255) NOT NULL default '',
        link_name varchar(255) NOT NULL default '',
        link_image varchar(255) NOT NULL default '',
        link_target varchar(25) NOT NULL default '',
        link_description varchar(255) NOT NULL default '',
        link_visible varchar(20) NOT NULL default 'Y',
        link_owner bigint(20) unsigned NOT NULL default '1',
        link_rating int(11) NOT NULL default '0',
        link_updated datetime NOT NULL default '0000-00-00 00:00:00',
        link_rel varchar(255) NOT NULL default '',
        link_notes mediumtext NOT NULL,
        link_rss varchar(255) NOT NULL default '',
        PRIMARY KEY  (link_id),
        KEY link_visible (link_visible));
    ''')

    cursor.execute('''CREATE TABLE wp_options (
        option_id bigint(20) unsigned NOT NULL auto_increment,
        option_name varchar(191) NOT NULL default '',
        option_value longtext NOT NULL,
        autoload varchar(20) NOT NULL default 'yes',
        PRIMARY KEY  (option_id),
        UNIQUE KEY option_name (option_name),
        KEY autoload (autoload));
    ''')

    cursor.execute('''CREATE TABLE wp_postmeta (
        meta_id bigint(20) unsigned NOT NULL auto_increment,
        post_id bigint(20) unsigned NOT NULL default '0',
        meta_key varchar(255) default NULL,
        meta_value longtext,
        PRIMARY KEY  (meta_id),
        KEY post_id (post_id),
        KEY meta_key (meta_key));
    ''')

    cursor.execute('''CREATE TABLE wp_posts (
        ID bigint(20) unsigned NOT NULL auto_increment,
        post_author bigint(20) unsigned NOT NULL default '0',
        post_date datetime NOT NULL default '0000-00-00 00:00:00',
        post_date_gmt datetime NOT NULL default '0000-00-00 00:00:00',
        post_content longtext NOT NULL,
        post_title text NOT NULL,
        post_excerpt text NOT NULL,
        post_status varchar(20) NOT NULL default 'publish',
        comment_status varchar(20) NOT NULL default 'open',
        ping_status varchar(20) NOT NULL default 'open',
        post_password varchar(255) NOT NULL default '',
        post_name varchar(200) NOT NULL default '',
        to_ping text NOT NULL,
        pinged text NOT NULL,
        post_modified datetime NOT NULL default '0000-00-00 00:00:00',
        post_modified_gmt datetime NOT NULL default '0000-00-00 00:00:00',
        post_content_filtered longtext NOT NULL,
        post_parent bigint(20) unsigned NOT NULL default '0',
        guid varchar(255) NOT NULL default '',
        menu_order int(11) NOT NULL default '0',
        post_type varchar(20) NOT NULL default 'post',
        post_mime_type varchar(100) NOT NULL default '',
        comment_count bigint(20) NOT NULL default '0',
        PRIMARY KEY  (ID),
        KEY post_name (post_name),
        KEY type_status_date (post_type,post_status,post_date,ID),
        KEY post_parent (post_parent),
        KEY post_author (post_author));
    ''')

    cursor.execute('''CREATE TABLE wp_term_relationships (
    object_id bigint(20) unsigned NOT NULL default 0,
    term_taxonomy_id bigint(20) unsigned NOT NULL default 0,
    term_order int(11) NOT NULL default 0,
    PRIMARY KEY  (object_id,term_taxonomy_id),
    KEY term_taxonomy_id (term_taxonomy_id));
    ''')

    cursor.execute('''CREATE TABLE wp_term_taxonomy (
    term_taxonomy_id bigint(20) unsigned NOT NULL auto_increment,
    term_id bigint(20) unsigned NOT NULL default 0,
    taxonomy varchar(32) NOT NULL default '',
    description longtext NOT NULL,
    parent bigint(20) unsigned NOT NULL default 0,
    count bigint(20) NOT NULL default 0,
    PRIMARY KEY  (term_taxonomy_id),
    UNIQUE KEY term_id_taxonomy (term_id,taxonomy),
    KEY taxonomy (taxonomy));
    ''')

    cursor.execute('''CREATE TABLE wp_termmeta (
        meta_id bigint(20) unsigned NOT NULL auto_increment,
        term_id bigint(20) unsigned NOT NULL default '0',
        meta_key varchar(255) default NULL,
        meta_value longtext,
        PRIMARY KEY  (meta_id),
        KEY term_id (term_id),
        KEY meta_key (meta_key));
    ''')

    cursor.execute('''CREATE TABLE wp_terms (
    term_id bigint(20) unsigned NOT NULL auto_increment,
    name varchar(200) NOT NULL default '',
    slug varchar(200) NOT NULL default '',
    term_group bigint(10) NOT NULL default 0,
    PRIMARY KEY  (term_id),
    KEY slug (slug),
    KEY name (name));
    ''')

    cursor.execute('''CREATE TABLE wp_usermeta (
        umeta_id bigint(20) unsigned NOT NULL auto_increment,
        user_id bigint(20) unsigned NOT NULL default '0',
        meta_key varchar(255) default NULL,
        meta_value longtext,
        PRIMARY KEY  (umeta_id),
        KEY user_id (user_id),
        KEY meta_key (meta_key));
    ''')

    cursor.execute('''CREATE TABLE wp_users (
        ID bigint(20) unsigned NOT NULL auto_increment,
        user_login varchar(60) NOT NULL default '',
        user_pass varchar(255) NOT NULL default '',
        user_nicename varchar(50) NOT NULL default '',
        user_email varchar(100) NOT NULL default '',
        user_url varchar(100) NOT NULL default '',
        user_registered datetime NOT NULL default '0000-00-00 00:00:00',
        user_activation_key varchar(255) NOT NULL default '',
        user_status int(11) NOT NULL default '0',
        display_name varchar(250) NOT NULL default '',
        PRIMARY KEY  (ID),
        KEY user_login_key (user_login),
        KEY user_nicename (user_nicename),
        KEY user_email (user_email));
    ''')


    # add admin user

    cursor.execute('SELECT CURRENT_TIMESTAMP()')
    registered_time = cursor.fetchone()[0]
    registered_time = str(registered_time)

    cursor.execute('''INSERT INTO wp_users (user_login, user_pass, user_email, user_nicename, display_name, user_registered)
    VALUES ('{}', MD5('{}'), 'admin@sandbox.blogvault.com', '{}', '{}', '{}');
    '''.format(admin, admin_pass, admin, admin, registered_time))

    cursor.execute("SELECT ID FROM wp_users ORDER BY ID DESC LIMIT 1")
    user_id = cursor.fetchone()[0]

    cursor.execute('''INSERT INTO wp_usermeta (umeta_id, user_id, meta_key, meta_value)
    VALUES (NULL, {}, 'wp_capabilities', 'a:1:{{s:13:"administrator";s:1:"1";}}');'''.format(user_id))

    cursor.execute('''INSERT INTO wp_usermeta (umeta_id, user_id, meta_key, meta_value)
    VALUES (NULL, {}, 'wp_user_level', 10);'''.format(user_id))



def populate_wp_options(cursor, db_name):
    cursor.execute('''Insert into wp_options(option_name, option_value, autoload)
    VALUES
    ('siteurl', 'http://'''+HOST+'/'+db_name+'''', 'yes'),
    ('home', 'http://'''+HOST+'/'+db_name+'''', 'yes'),
    ('blogname',' '''+db_name+'''' , 'yes'),
    ('blogdescription', 'Welcome to another Blogvault sandbox wordpress site', 'yes'),
    ('users_can_register', 0, 'yes'),
    ('admin_email', 'admin@sandbox.blogvault.com', 'yes'),
    ('start_of_week', 1, 'yes'),
    ('use_balanceTags', 0, 'yes'),
    ('use_smilies', 1, 'yes'),
    ('require_name_email', 1, 'yes'),
    ('comments_notify', 1, 'yes'),
    ('posts_per_rss' , 10, 'yes'),
    ('rss_use_excerpt' , 0, 'yes'),
    ('mailserver_url', 'mail.example.com', 'yes'),
    ('mailserver_login', 'login@example.com', 'yes'),
    ('mailserver_pass', 'password', 'yes'),
    ('mailserver_port', 110, 'yes'),
    ('default_category', 1, 'yes'),
    ('default_comment_status', 'open', 'yes'),
    ('default_ping_status', 'open', 'yes'),
    ('default_pingback_flag', 1, 'yes'),
    ('posts_per_page', 10, 'yes'),
    ('date_format', 'F j, Y', 'yes'),
    ('time_format', 'g:i a', 'yes'),
    ('links_updated_date_format', 'F j, Y g:i a', 'yes'),
    ('comment_moderation', 0, 'yes'),
    ('moderation_notify', 1, 'yes'),
    ('permalink_structure', '', 'yes'),
    ('rewrite_rules', '', 'yes'),
    ('hack_file', 0, 'yes'),
    ('blog_charset', 'UTF-8', 'yes'),
    ('moderation_keys', '', 'no'),
    ('active_plugins', 'a:0:{}', 'yes'),
    ('category_base', '', 'yes'),
    ('ping_sites', 'http://rpc.pingomatic.com/', 'yes'),
    ('comment_max_links', 2, 'yes'),
    ('gmt_offset', 0, 'yes'),
    ('default_email_category', 1, 'yes'),
    ('recently_edited', '', 'no'),
    ('template', 'twentytwenty', 'yes'),
    ('stylesheet', 'twentytwenty', 'yes'),
    ('comment_registration', 0, 'yes'),
    ('html_type', 'text/html', 'yes'),
    ('use_trackback', 0, 'yes'),
    ('default_role', 'subscriber', 'yes'),
    ('db_version', 49752, 'yes'),
    ('uploads_use_yearmonth_folders', 1, 'yes'),
    ('upload_path', '', 'yes'),
    ('blog_public', '1', 'yes'),
    ('default_link_category', 2, 'yes'),
    ('show_on_front', 'posts', 'yes'),
    ('tag_base', '', 'yes'),
    ('show_avatars', '1', 'yes'),
    ('avatar_rating', 'G', 'yes'),
    ('upload_url_path', '', 'yes'),
    ('thumbnail_size_w', 150, 'yes'),
    ('thumbnail_size_h', 150, 'yes'),
    ('thumbnail_crop', 1, 'yes'),
    ('medium_size_w', 300, 'yes'),
    ('medium_size_h', 300, 'yes'),
    ('avatar_default', 'mystery', 'yes'),
    ('large_size_w', 1024, 'yes'),
    ('large_size_h', 1024, 'yes'),
    ('image_default_link_type', 'none', 'yes'),
    ('image_default_size', '', 'yes'),
    ('image_default_align', '', 'yes'),
    ('close_comments_for_old_posts', 0, 'yes'),
    ('close_comments_days_old', 14, 'yes'),
    ('thread_comments', 1, 'yes'),
    ('thread_comments_depth', 5, 'yes'),
    ('page_comments', 0, 'yes'),
    ('comments_per_page', 50, 'yes'),
    ('default_comments_page', 'newest', 'yes'),
    ('comment_order', 'asc', 'yes'),
    ('sticky_posts', 'a:0:{}', 'yes'),
    ('widget_categories', 'a:0:{}', 'yes'),
    ('widget_text', 'a:0:{}', 'yes'),
    ('widget_rss', 'a:0:{}', 'yes'),
    ('uninstall_plugins', 'a:0:{}', 'no'),
    ('timezone_string', '', 'yes'),
    ('page_for_posts', 0, 'yes'),
    ('page_on_front', 0, 'yes'),
    ('default_post_format', 0, 'yes'),
    ('link_manager_enabled', 0, 'yes'),
    ('finished_splitting_shared_terms', 1, 'yes'),
    ('site_icon', 0, 'yes'),
    ('medium_large_size_w', 768, 'yes'),
    ('medium_large_size_h', 0, 'yes'),
    ('wp_page_for_privacy_policy', 0, 'yes'),
    ('show_comments_cookies_opt_in', 1, 'yes'),
    ('admin_email_lifespan', '1612222386', 'yes'),
    ('disallowed_keys', '', 'no'),
    ('comment_previously_approved', 1, 'yes'),
    ('auto_plugin_theme_update_emails', 'a:0:{}', 'no'),
    ('auto_update_core_dev', 'enabled', 'no'),
    ('auto_update_core_minor', 'enabled', 'no'),
    ('auto_update_core_major', 'enabled', 'no'),
    ('wp_user_roles', 'a:5:{s:13:"administrator";a:2:{s:4:"name";s:13:"Administrator";s:12:"capabilities";a:61:{s:13:"switch_themes";b:1;s:11:"edit_themes";b:1;s:16:"activate_plugins";b:1;s:12:"edit_plugins";b:1;s:10:"edit_users";b:1;s:10:"edit_files";b:1;s:14:"manage_options";b:1;s:17:"moderate_comments";b:1;s:17:"manage_categories";b:1;s:12:"manage_links";b:1;s:12:"upload_files";b:1;s:6:"import";b:1;s:15:"unfiltered_html";b:1;s:10:"edit_posts";b:1;s:17:"edit_others_posts";b:1;s:20:"edit_published_posts";b:1;s:13:"publish_posts";b:1;s:10:"edit_pages";b:1;s:4:"read";b:1;s:8:"level_10";b:1;s:7:"level_9";b:1;s:7:"level_8";b:1;s:7:"level_7";b:1;s:7:"level_6";b:1;s:7:"level_5";b:1;s:7:"level_4";b:1;s:7:"level_3";b:1;s:7:"level_2";b:1;s:7:"level_1";b:1;s:7:"level_0";b:1;s:17:"edit_others_pages";b:1;s:20:"edit_published_pages";b:1;s:13:"publish_pages";b:1;s:12:"delete_pages";b:1;s:19:"delete_others_pages";b:1;s:22:"delete_published_pages";b:1;s:12:"delete_posts";b:1;s:19:"delete_others_posts";b:1;s:22:"delete_published_posts";b:1;s:20:"delete_private_posts";b:1;s:18:"edit_private_posts";b:1;s:18:"read_private_posts";b:1;s:20:"delete_private_pages";b:1;s:18:"edit_private_pages";b:1;s:18:"read_private_pages";b:1;s:12:"delete_users";b:1;s:12:"create_users";b:1;s:17:"unfiltered_upload";b:1;s:14:"edit_dashboard";b:1;s:14:"update_plugins";b:1;s:14:"delete_plugins";b:1;s:15:"install_plugins";b:1;s:13:"update_themes";b:1;s:14:"install_themes";b:1;s:11:"update_core";b:1;s:10:"list_users";b:1;s:12:"remove_users";b:1;s:13:"promote_users";b:1;s:18:"edit_theme_options";b:1;s:13:"delete_themes";b:1;s:6:"export";b:1;}}s:6:"editor";a:2:{s:4:"name";s:6:"Editor";s:12:"capabilities";a:34:{s:17:"moderate_comments";b:1;s:17:"manage_categories";b:1;s:12:"manage_links";b:1;s:12:"upload_files";b:1;s:15:"unfiltered_html";b:1;s:10:"edit_posts";b:1;s:17:"edit_others_posts";b:1;s:20:"edit_published_posts";b:1;s:13:"publish_posts";b:1;s:10:"edit_pages";b:1;s:4:"read";b:1;s:7:"level_7";b:1;s:7:"level_6";b:1;s:7:"level_5";b:1;s:7:"level_4";b:1;s:7:"level_3";b:1;s:7:"level_2";b:1;s:7:"level_1";b:1;s:7:"level_0";b:1;s:17:"edit_others_pages";b:1;s:20:"edit_published_pages";b:1;s:13:"publish_pages";b:1;s:12:"delete_pages";b:1;s:19:"delete_others_pages";b:1;s:22:"delete_published_pages";b:1;s:12:"delete_posts";b:1;s:19:"delete_others_posts";b:1;s:22:"delete_published_posts";b:1;s:20:"delete_private_posts";b:1;s:18:"edit_private_posts";b:1;s:18:"read_private_posts";b:1;s:20:"delete_private_pages";b:1;s:18:"edit_private_pages";b:1;s:18:"read_private_pages";b:1;}}s:6:"author";a:2:{s:4:"name";s:6:"Author";s:12:"capabilities";a:10:{s:12:"upload_files";b:1;s:10:"edit_posts";b:1;s:20:"edit_published_posts";b:1;s:13:"publish_posts";b:1;s:4:"read";b:1;s:7:"level_2";b:1;s:7:"level_1";b:1;s:7:"level_0";b:1;s:12:"delete_posts";b:1;s:22:"delete_published_posts";b:1;}}s:11:"contributor";a:2:{s:4:"name";s:11:"Contributor";s:12:"capabilities";a:5:{s:10:"edit_posts";b:1;s:4:"read";b:1;s:7:"level_1";b:1;s:7:"level_0";b:1;s:12:"delete_posts";b:1;}}s:10:"subscriber";a:2:{s:4:"name";s:10:"Subscriber";s:12:"capabilities";a:2:{s:4:"read";b:1;s:7:"level_0";b:1;}}}', 'yes');
''')


def give_permissions(dbname, user, cursor):
    cursor.execute("GRANT ALL PRIVILEGES ON {} . * TO {}@'%';".format(dbname, user))
    cursor.execute("FLUSH PRIVILEGES;")

def db_main(DB_NAME, DB_USER, DB_PASSWORD, ADMIN, ADMIN_PASSWORD):
    try:
        logger.info("Creating database user: "+ DB_USER)
        mydb = conn_db('')
        mycursor = mydb.cursor()
        create_user(DB_USER, DB_PASSWORD, mycursor)
        logger.info("Creating database: "+ DB_NAME)
        create_db(DB_NAME, mycursor)
        for_create = conn_db(DB_NAME)
        create_cursor = for_create.cursor()
        logger.info("Adding tables and admin user")
        create_tables_and_add_user(DB_NAME, ADMIN, ADMIN_PASSWORD, create_cursor)
        logger.info("Populating wp_options")
        populate_wp_options(create_cursor, DB_NAME)
        for_create.commit()
        logger.info("Giving permission to user")
        give_permissions(DB_NAME, DB_USER, mycursor)
        mycursor.close()
        create_cursor.close()
        mydb.close()
        for_create.close()
    except mysql.connector.Error as error:
        logger.error(error)
        return 500
    logger.info("Created Database: "+ DB_NAME)
    return 200

def delete_db(DB_NAME, DB_USER):
    try:
        logger.info("DELETE REQUEST")
        mydb = conn_db('')
        mycursor = mydb.cursor()
        mycursor.execute('DROP DATABASE {}'.format(DB_NAME))
        logger.info("Database dropped: "+ DB_NAME)
        mycursor.execute('DROP USER {}'.format(DB_USER))
        logger.info("User dropped: "+ DB_USER)
        mycursor.close()
    except mysql.connector.Error as error:
        logger.error(error)
        return 500
    logger.info("Success")
    return 200



