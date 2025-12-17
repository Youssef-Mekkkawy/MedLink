"""
Database Configuration
"""

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'medlink_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False
}

# Database Settings
DB_SETTINGS = {
    'auto_create': True,
    'auto_migrate': True,
    'drop_if_exists': False,
    'import_json_data': True,
    'generate_test_data': False
}
