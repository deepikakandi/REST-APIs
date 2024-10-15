import psycopg2
import logging

def get_db_connection():
    try:
        logging.info('Attempting to connect to the database...')
        
        connection = psycopg2.connect(host='localhost', dbname ='organization_database', user ='postgres', password = 'MOMdad21*',port = 5434)
        logging.info('Database connection successful.')
        return connection
    
    except Exception as e:
        logging.error(f'Database connection failed: {e}')
        raise


    