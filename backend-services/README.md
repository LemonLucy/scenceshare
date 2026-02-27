# SceneShare MSA Backend

## 🏗️ 구조

```
backend-services/
├── square/      (Port 8001) - 커뮤니티 포스팅
├── critics/     (Port 8002) - 평론가 리뷰
├── archive/     (Port 8003) - 인터뷰 아카이브
└── gateway/     (Port 9000) - API Gateway
```

## 🚀 실행

```bash
bash start-services.sh
```

## 📍 Square Service API

### 게시글
- `GET /api/v1/square/posts?sort=recent` - 최신순 (전체)
- `GET /api/v1/square/posts?sort=popular` - 인기순 (전체)
- `GET /api/v1/square/posts?movie_id=550` - 특정 영화 게시글
- `POST /api/v1/square/posts` - 게시글 작성
- `GET /api/v1/square/posts/{id}` - 게시글 상세 (댓글 포함)
- `POST /api/v1/square/posts/{id}/like` - 좋아요
- `DELETE /api/v1/square/posts/{id}` - 삭제

### 댓글
- `GET /api/v1/square/posts/{id}/comments` - 댓글 목록
- `POST /api/v1/square/posts/{id}/comments` - 댓글 작성
- `POST /api/v1/square/comments/{id}/like` - 댓글 좋아요

### 통계
- `GET /api/v1/square/stats/movies` - 영화별 게시글 통계

## 🎯 특징

- ✅ Most Recent: 전체 게시글 최신순
- ✅ Most Popular: 전체 게시글 인기순 (좋아요)
- ✅ Movie Filter: 영화별 게시글 필터링
- ✅ 댓글 시스템
- ✅ 좋아요 기능
