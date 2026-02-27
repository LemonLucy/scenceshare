# SceneShare - Global Movie Community PWA

글로벌 영화 커뮤니티 플랫폼

## 📁 프로젝트 구조

```
/home/lucy/Q/movie/
├── .env                      # 환경변수 (TMDB API Key)
├── frontend/                 # Next.js 프론트엔드 (Port 3000)
└── backend-services/         # MSA 백엔드
    ├── movies/              # TMDB 영화 서비스 (Port 8000)
    ├── square/              # 커뮤니티 포스팅 (Port 8001)
    ├── critics/             # 평론가 리뷰 (Port 8002)
    ├── archive/             # 인터뷰 아카이브 (Port 8003)
    ├── gateway/             # API Gateway (Port 9000)
    └── start-services.sh    # 전체 서비스 실행 스크립트
```

## 🚀 실행 방법

### 백엔드 서비스 시작
```bash
cd /home/lucy/Q/movie/backend-services
bash start-services.sh
```

### 프론트엔드 시작
```bash
cd /home/lucy/Q/movie/frontend
npm run dev
```

## 🌐 서비스 URL

- **프론트엔드**: http://localhost:3000
- **API Gateway**: http://localhost:9000
- **API Docs**: http://localhost:9000/docs

## 🔑 환경변수

`/home/lucy/Q/movie/.env`:
```
TMDB_API_KEY=7394c0d4d8e4eb4b65728ea9d83ff3d8
```

## 📊 구현된 기능

### Frontend
- ✅ 홈페이지 (트렌딩 영화)
- ✅ The Square (커뮤니티)
  - Most Recent (최신순)
  - Most Popular (인기순)
  - Movies (영화별)
- ✅ 영화별 포스팅 페이지
- ✅ Critic's View (UI)
- ✅ The Archive (UI)
- ✅ Profile (UI)

### Backend (MSA)
- ✅ Movies Service (TMDB API)
- ✅ Square Service (포스팅, 댓글)
- ✅ Critics Service
- ✅ Archive Service
- ✅ API Gateway

## 🛠️ 기술 스택

- **Frontend**: Next.js 16, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **External**: TMDB API
- **Architecture**: Microservices (MSA)

## 📝 다음 작업

1. 포스트 작성 페이지
2. 포스트 상세 + 댓글 UI
3. 인증 시스템
4. Critics/Archive 데이터 추가
