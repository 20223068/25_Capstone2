from sentence_transformers import SentenceTransformer
import pymysql
import json

def run(story_title=None):
    """
    story_title이 주어지면 해당 동화만 임베딩,
    없으면 모든 문단을 임베딩합니다.
    """
    # 1. 모델 로딩
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ 임베딩 모델 로딩 완료!")

    # 2. DB 연결
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        db="fairy_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # 3. 임베딩이 비어 있는 문단 불러오기
    if story_title:
        print(f"🎯 '{story_title}' 동화 문단만 임베딩합니다.")
        cursor.execute("""
            SELECT id, chunk_text 
            FROM story_chunks 
            WHERE story_title = %s AND embedding IS NULL
        """, (story_title,))
    else:
        print("🎯 모든 동화의 문단을 임베딩합니다.")
        cursor.execute("""
            SELECT id, chunk_text 
            FROM story_chunks 
            WHERE embedding IS NULL
        """)

    chunks = cursor.fetchall()
    print(f"🔍 임베딩할 문단 수: {len(chunks)}")

    # 4. 임베딩 수행 + DB 저장
    for chunk in chunks:
        emb = model.encode(chunk["chunk_text"]).tolist()  # numpy → list
        emb_json = json.dumps(emb, ensure_ascii=False)

        cursor.execute(
            "UPDATE story_chunks SET embedding = %s WHERE id = %s",
            (emb_json, chunk["id"])
        )

    conn.commit()
    conn.close()

    print("🎉 모든 문단 임베딩이 완료되어 DB에 저장되었습니다.")
