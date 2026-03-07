from bs4 import BeautifulSoup
import pymysql
import os

def extract_chunks(html_path):
    """HTML 파일에서 <div class='story-slide'> 문단 텍스트 추출"""
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    slides = soup.select("div.story-slide")
    chunks = [s.get_text(separator=" ", strip=True) for s in slides if s.get_text(strip=True)]
    print(f"📖 {os.path.basename(html_path)} → 슬라이드 {len(slides)}개 / 추출된 문단 {len(chunks)}개")
    return chunks


def run():
    # === 1. 동화 목록 정의 ===
    fairy_tales = [
        {"title": "나비의 꿈", "file": "templates/ButterflyDream.html"},
        {"title": "성냥팔이소녀", "file": "templates/LittleMatch.html"}
    ]

    # === 2. DB 연결 ===
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        db="fairy_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # 기존 문단 삭제
    cursor.execute("DELETE FROM story_chunks")
    print("🧹 story_chunks 테이블 초기화 완료")

    # === 3. 각 동화별로 문단 저장 ===
    total_chunks = 0
    for story in fairy_tales:
        story_title = story["title"]
        file_path = story["file"]

        if not os.path.exists(file_path):
            print(f"⚠️ 파일 없음: {file_path}")
            continue

        chunks = extract_chunks(file_path)

        for chunk in chunks:
            cursor.execute(
                "INSERT INTO story_chunks (story_title, chunk_text) VALUES (%s, %s)",
                (story_title, chunk)
            )
        total_chunks += len(chunks)
        print(f"✅ '{story_title}' 저장 완료 ({len(chunks)}개 문단)")

    conn.commit()
    conn.close()

    print(f"🎉 전체 완료: {total_chunks}개의 문단이 story_chunks 테이블에 저장되었습니다.")