-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url VARCHAR(500),
    bio TEXT,
    preferred_language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movies Table (cached from TMDB)
CREATE TABLE movies (
    id INTEGER PRIMARY KEY, -- TMDB ID
    title VARCHAR(500) NOT NULL,
    original_title VARCHAR(500),
    overview TEXT,
    poster_path VARCHAR(500),
    backdrop_path VARCHAR(500),
    release_date DATE,
    runtime INTEGER,
    vote_average DECIMAL(3,1),
    genres JSONB, -- [{id: 28, name: "Action"}]
    tmdb_data JSONB, -- full TMDB response cache
    last_synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Square Posts (Community Discussion)
CREATE TABLE square_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    movie_id INTEGER REFERENCES movies(id) ON DELETE SET NULL,
    title VARCHAR(300) NOT NULL,
    content TEXT NOT NULL,
    post_type VARCHAR(20) DEFAULT 'discussion', -- discussion, question, review
    language VARCHAR(10) DEFAULT 'en',
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Square Comments
CREATE TABLE square_comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES square_posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    parent_comment_id INTEGER REFERENCES square_comments(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Critics Reviews (Expert/YouTuber perspectives)
CREATE TABLE critics_reviews (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    critic_name VARCHAR(200) NOT NULL,
    critic_type VARCHAR(50), -- professional, youtuber, blogger
    source_name VARCHAR(200), -- publication or channel name
    source_url VARCHAR(500),
    youtube_video_id VARCHAR(50),
    rating DECIMAL(3,1),
    summary TEXT,
    full_text TEXT,
    language VARCHAR(10) DEFAULT 'en',
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Archive Interviews
CREATE TABLE archive_interviews (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE SET NULL,
    title VARCHAR(500) NOT NULL,
    interviewee_name VARCHAR(200) NOT NULL,
    interviewee_role VARCHAR(100), -- director, actor, producer
    youtube_video_id VARCHAR(50),
    source_url VARCHAR(500),
    description TEXT,
    tags JSONB, -- ["behind-the-scenes", "casting"]
    language VARCHAR(10) DEFAULT 'en',
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Likes (for posts and comments)
CREATE TABLE user_likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL, -- post, comment
    target_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, target_type, target_id)
);

-- User Watchlist
CREATE TABLE user_watchlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'want_to_watch', -- want_to_watch, watching, watched
    rating DECIMAL(3,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, movie_id)
);

-- Indexes for performance
CREATE INDEX idx_square_posts_movie ON square_posts(movie_id);
CREATE INDEX idx_square_posts_created ON square_posts(created_at DESC);
CREATE INDEX idx_square_comments_post ON square_comments(post_id);
CREATE INDEX idx_critics_reviews_movie ON critics_reviews(movie_id);
CREATE INDEX idx_archive_interviews_movie ON archive_interviews(movie_id);
CREATE INDEX idx_user_likes_target ON user_likes(target_type, target_id);
