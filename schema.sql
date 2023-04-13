CREATE TABLE IF NOT EXISTS characters(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game TEXT NOT NULL,
    name TEXT NOT NULL,
    frame_data TEXT
);

CREATE TABLE IF NOT EXISTS characters(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    analysis_results TEXT
);