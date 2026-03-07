CREATE DATABASE IF NOT EXISTS fairy_db;
USE fairy_db;

-- 1. 질문 테이블 --
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    story_title VARCHAR(100) NOT NULL,
    questions TEXT,
    page_num INT
);

-- 2. 답변 테이블 --
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT,
    answers TEXT,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- 3. 질문 임베딩 테이블 --
CREATE TABLE question_embeddings (
    question_id INT PRIMARY KEY,
    embedding JSON,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- 4. 동화 문단 나누는 테이블 --
CREATE TABLE story_chunks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    story_title VARCHAR(100) NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding JSON DEFAULT NULL
);


-- (신규 DB) --

-- [신규 1] 퀴즈-답변 (Quiz_question) --
CREATE TABLE quiz_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    story_title VARCHAR(100) NOT NULL,   -- 어떤 동화인지
    child_name VARCHAR(50) NULL,         -- 아이 이름 (선택)
    child_age INT NOT NULL,              -- 아이 나이 (선택)
    question_texts JSON,                 -- 질문 목록 (JSON 배열)
    answers JSON,                        -- 각 질문에 대한 답변 (JSON 배열)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- [신규 2] GPT 부모 피드백 (quiz_activity 테이블 기반) --
CREATE TABLE quiz_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    story_title VARCHAR(100) NOT NULL,
    child_name VARCHAR(50) NULL,
    child_age TINYINT NULL,

    -- 세 항목 평가
    comprehension_score TINYINT,       -- 이해력 별점
    comprehension_comment TEXT,        -- 이해력 한줄평
    creativity_score TINYINT,          -- 창의성 별점
    creativity_comment TEXT,           -- 창의성 한줄평
    expression_score TINYINT,          -- 표현력 별점
    expression_comment TEXT,           -- 표현력 한줄평

    -- 전체 평가 (칭찬 + 아쉬운점)
    overall_comment TEXT,              -- 예: "👍 문장을 잘 이해했어요. 🌱 조금 더 다양하게 표현해보세요."

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES quiz_activity(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);