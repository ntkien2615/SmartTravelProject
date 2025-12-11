-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create schedules table
-- Note: user_id type must match users.id type. 
-- If users.id is UUID, use UUID. If Integer, use BIGINT.
CREATE TABLE IF NOT EXISTS schedules (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE, -- Adjusted for Integer User IDs
    destination TEXT,
    budget NUMERIC,
    start_time TEXT,
    end_time TEXT,
    timeline_json TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Disable RLS for simple custom auth
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE schedules DISABLE ROW LEVEL SECURITY;
