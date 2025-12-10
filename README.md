# Call System (Portfolio Project)

React(Next.js) + Python(FastAPI) + MySQL + FreeSWITCH 기반 콜 시스템 포트폴리오 프로젝트입니다.  
로컬 개발 환경에서 콜 데이터 생성, 조회, 통계 API까지 구현되는 것을 목표로 합니다.

---

## 📁 Project Structure

CALL-SYSTEM/
├── backend/            # FastAPI 백엔드
│    ├── app/
│    │    ├── core/     # DB 연결 등 공통 모듈
│    │    ├── models/   # SQLAlchemy 모델
│    │    ├── services/ # 도메인 서비스 로직
│    │    └── main.py   # FastAPI 엔트리포인트
│    └── requirements.txt
│
├── frontend/           # Next.js 프론트엔드
│    └── (초기 셋업)
│
├── docker-compose.yml  # MySQL, FreeSWITCH 컨테이너 구성
├── README.md
└── .gitignore

---

## 💾 Local Development Setup

### 1) Docker 실행 (MySQL, FreeSWITCH)

docker compose up -d

### 2) Backend 실행 (FastAPI)

cd backend
uvicorn app.main:app --reload

### 3) Frontend 실행 (Next.js)

cd frontend
npm install
npm run dev

## 🗄 Database Schema (최초 버전)

콜 데이터 저장용 기본 테이블: 현재 세팅중...