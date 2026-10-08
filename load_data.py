import sqlite3
import pandas as pd
import os

def init_db():
    db_name = 'cell-count.db'
    csv_file = 'cell-count.csv'
    
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Error: {csv_file} not found in the current directory.")

    df = pd.read_csv(csv_file)
    
    metadata_cols = [
        'sample', 'project', 'subject', 'condition', 'age', 'sex', 
        'treatment', 'response', 'sample_type', 'time_from_treatment_start'
    ]
    cell_cols = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    
    samples_df = df[metadata_cols].copy()
    
    cell_counts_df = df.melt(
        id_vars=['sample'], 
        value_vars=cell_cols, 
        var_name='population', 
        value_name='count'
    )
    
    conn = sqlite3.connect(db_name)
    
    samples_df.to_sql('samples', conn, if_exists='replace', index=False)
    cell_counts_df.to_sql('cell_counts', conn, if_exists='replace', index=False)
    
    cursor = conn.cursor()
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sample ON cell_counts("sample");')
    conn.commit()
    conn.close()
    
    print(f"Database '{db_name}' successfully created and populated.")

if __name__ == "__main__":
    init_db()