# SceneShare - 구현 가이드 및 권장사항

## 🔐 보안 (Security)

### JWT 인증
- Access Token: 15분 만료
- Refresh Token: 7일 만료, httpOnly 쿠키에 저장
- bcrypt로 비밀번호 해싱 (rounds=12)

### CORS 설정
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sceneshare.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting
- Redis 기반 rate limiting
- 게시글 작성: 10/hour per user
- API 호출: 100/minute per IP

---

## 🚀 성능 최적화 (Performance)

### 캐싱 전략
1. **Redis 캐싱**
   - TMDB API 응답: 24시간
   - 인기 게시글 목록: 5분
   - 영화 상세 정보: 1시간

2. **CDN**
   - 영화 포스터/배경 이미지는 CloudFront 또는 Cloudflare 사용
   - Static assets (JS, CSS) CDN 배포

3. **Database Indexing**
   - 이미 schema에 주요 인덱스 포함
   - 추가로 full-text search 필요시 PostgreSQL의 `tsvector` 사용

### 이미지 최적화
- Next.js Image 컴포넌트 사용 (자동 최적화)
- TMDB 이미지는 적절한 크기로 요청 (w500, w780 등)
- WebP 포맷 우선 사용

---

## 📱 PWA 체크리스트

### 필수 요소
- [x] manifest.json 설정
- [x] Service Worker 구현
- [ ] HTTPS 적용 (프로덕션 필수)
- [ ] Offline 페이지 제작
- [ ] 앱 아이콘 생성 (72px ~ 512px)
- [ ] Apple Touch Icon 추가
- [ ] meta 태그 설정

### HTML Head 설정
```html
<meta name="theme-color" content="#1e40af">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="/icons/icon-192x192.png">
<link rel="manifest" href="/manifest.json">
```

### Lighthouse PWA 점수 목표
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 100
- PWA: 100

---

## 🌐 글로벌 대응

### 다국어 우선순위
1. 영어 (en) - 기본
2. 한국어 (ko)
3. 일본어 (ja)
4. 스페인어 (es)
5. 프랑스어 (fr)

### 지역별 고려사항
- 날짜/시간 포맷: `Intl.DateTimeFormat` 사용
- 숫자 포맷: 천 단위 구분자 지역별 적용
- RTL 언어 지원 준비 (아랍어 등)

### TMDB 다국어 지원
- TMDB API는 `language` 파라미터로 다국어 지원
- 유저의 `preferred_language`에 따라 API 호출
- 번역 없는 경우 영어로 fallback

---

## 🗄️ 데이터베이스 마이그레이션

### Alembic 설정
```bash
# 초기 마이그레이션 생성
alembic init alembic

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial schema"

# 마이그레이션 적용
alembic upgrade head
```

### 백업 전략
- 일일 자동 백업 (AWS RDS 자동 백업)
- 주간 스냅샷
- 중요 업데이트 전 수동 백업

---

## 📊 모니터링 & 분석

### 추천 도구
- **Backend**: Sentry (에러 트래킹), Prometheus + Grafana (메트릭)
- **Frontend**: Google Analytics 4, Vercel Analytics
- **Performance**: Lighthouse CI, Web Vitals

### 주요 메트릭
- API 응답 시간
- 게시글 작성/조회 수
- 활성 사용자 수 (DAU/MAU)
- 영화별 토론 활성도
- PWA 설치율

---

## 🧪 테스트 전략

### Backend
```python
# pytest + pytest-asyncio
# tests/test_square.py
async def test_create_post(client, auth_headers):
    response = await client.post(
        "/api/v1/square/posts",
        json={"title": "Test", "content": "Test content"},
        headers=auth_headers
    )
    assert response.status_code == 200
```

### Frontend
- Jest + React Testing Library
- Cypress (E2E 테스트)
- Playwright (크로스 브라우저 테스트)

---

## 🚢 배포 전략

### 추천 인프라
- **Backend**: AWS ECS/Fargate 또는 Railway/Render
- **Frontend**: Vercel 또는 Netlify
- **Database**: AWS RDS PostgreSQL
- **Cache**: AWS ElastiCache Redis
- **Storage**: AWS S3 (유저 업로드 이미지)

### CI/CD
- GitHub Actions
- 자동 테스트 → 스테이징 배포 → 프로덕션 배포
- 환경별 환경변수 관리 (.env.production, .env.staging)

---

## 📝 개발 우선순위

### Phase 1 (MVP - 4주)
1. 기본 인증 시스템
2. TMDB API 연동
3. The Square 기본 기능 (게시글 CRUD)
4. 영화 상세 페이지
5. 반응형 UI

### Phase 2 (확장 - 4주)
1. Critic's View 구현
2. The Archive 구현
3. 댓글 시스템
4. 좋아요/북마크 기능
5. 유저 프로필

### Phase 3 (최적화 - 2주)
1. PWA 완성
2. 성능 최적화
3. SEO 최적화
4. 다국어 지원 확대
5. 모니터링 설정

---

## 🔧 환경변수 예시

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/sceneshare
REDIS_URL=redis://localhost:6379
TMDB_API_KEY=your_tmdb_key
YOUTUBE_API_KEY=your_youtube_key
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000,https://sceneshare.com
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_TMDB_IMAGE_BASE=https://image.tmdb.org/t/p
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```
