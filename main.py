import os

current_dir = os.getcwd()
final_dir = os.path.join(current_dir, 'all_databas')

def db_file_path(path:str):
    if not os.path.exists(final_dir):
       os.makedirs(final_dir)
    db_path = os.path.join(final_dir, path)
    return db_path