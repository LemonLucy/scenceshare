# SceneShare Backend

FastAPI 백엔드 서버

## 실행 방법

```bash
# 가상환경 활성화
source venv/bin/activate

# 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API 문서

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 엔드포인트

### Movies
- `GET /api/v1/movies/trending` - 트렌딩 영화
- `GET /api/v1/movies/search?q=query` - 영화 검색
- `GET /api/v1/movies/{movie_id}` - 영화 상세

### Square (커뮤니티)
- `GET /api/v1/square/posts` - 게시글 목록
- `POST /api/v1/square/posts` - 게시글 작성
- `GET /api/v1/square/posts/{post_id}` - 게시글 상세

### Critics
- `GET /api/v1/critics/reviews` - 평론가 리뷰 목록

### Archive
- `GET /api/v1/archive/interviews` - 인터뷰 목록

## 환경 변수

`.env` 파일에서 설정:
- `TMDB_API_KEY` - TMDB API 키
- `YOUTUBE_API_KEY` - YouTube API 키
- `DATABASE_URL` - 데이터베이스 URL
