# 🌐PiroTime

#### 🏆피로그래밍 21기 최종 프로젝트 작품

## 🌟Overview

세상 곳곳의 피로그래머들을 연결하는 피로그래밍 커뮤니티 플랫폼 입니다.

## 🌟PiroTime 플랫폼 링크

[플랫폼 링크](https://pirotime.com/)

## 🌟협업 페이지 링크

[노션 링크](https://www.notion.so/PiroTime-5d7fb0a939be45ee9e663767952b0b3c)

## 🖥️서비스 화면

### 모든 페이지 모바일(아이폰 14 Pro Max 기준 max-width: 430px) 반응형 지원

#### 홈(랜딩페이지)

- 피로그래밍 로고 적용
- 로그인 및 회원가입 버튼 생성
- 'About PiroTime' 으로 플랫폼 소개
- 주요 기능을 나열

![PiroTime - Chrome 2024-08-19 20-13-35](https://github.com/user-attachments/assets/d48131a4-27b9-4750-bf4e-23772d2123e2)

#### 회원가입 & 로그인 & 로그아웃

- 유저 회원가입/로그인
- 회원가입/로그인을 하면 start 페이지로 넘어간다.

#### 시작 페이지

- 각 게시판 인기글 확인 가능
- 커피챗 다수 진행한 선배님 확인 가능

![PiroTime - Chrome 2024-08-19 20-13-35](https://github.com/user-attachments/assets/fea7856a-9d8c-4922-accf-8d8489359861)

#### 커피챗

- 커피챗 프로필 등록
- 커피챗 신청
- 커피챗 프로필 기수별 확인
- 커피챗 리뷰 작성/관리

![PiroTime - Chrome 2024-08-19 20-13-35](https://github.com/user-attachments/assets/8e6a1eeb-da33-46ce-9404-647d685f37df)

#### 프로젝트 리뷰

- 프로젝트 리뷰/피드백을 받는 공간이다.
- 게시판 CRUD
- 깃허브 URL 등록
- 북마크/좋아요 -> 마이페이지에서 확인 가능

![PiroTime - Chrome 2024-08-19 20-13-35](https://github.com/user-attachments/assets/a658414d-f1f5-4445-b79a-bd37cfb849fc)

#### 프로젝트 협업

- 프로젝트 협업을 제안하는 공간이다.
- 협업을 원한다면 메일을 통해 협업에 함께 할 수 있다.
- 게시판 CRUD
- 북마크/좋아요 -> 마이페이지에서 확인 가능

![PiroTime - Chrome 2024-08-19 20-13-35](https://github.com/user-attachments/assets/2761259c-ddbf-475a-ae89-38004b849c4c)

#### IT 동향

- IT 동향을 공유하는 공간이다
- 게시판 CRUD
- 북마크/좋아요 -> 마이페이지에서 확인 가능

![PiroTime - Chrome 2024-08-19 20-13-35](https://github.com/user-attachments/assets/6ab2729d-eae8-4c35-a9c9-d11e374a93a6)

#### 마이페이지

- 내가 쓴 글/ 좋아요/ 북마크 기록 확인
- 커피챗 수락/거절 기능

![PiroTime - Chrome 2024-08-19 20-13-35](https://github.com/user-attachments/assets/d6161b74-0997-43a7-bdff-bccf9e4b7e78)

## 🎯주요 기능

- 게시판 기능(create, detail, update,list)
- 각 게시판 인기글 모아보기 기능
- 1:1 매칭 기능(Accepted, Rejected)
- 메일 회원 정보 송신 기능
- 리뷰 관리 기능
- 내 정보 관리 기능
- 사용자 친화적 UI

## 🔨개발 환경

#### Management Tool

- 코드 관리: Git
- 커뮤니케이션: Zep, Notion
- 디자인: Figma

#### 🐳Backend

- Python `3.8.0`
- Django `4.2.x`
- Django Rest Framework `3.12.x`
- Gunicorn `20.1.0` (배포용 WSGI 서버)
- PostgreSQL `16.4.x`

#### 🦊Frontend

- lang: HTML5, CSS3, JAVASCRIPT

#### 🗂️DB

- PostgreSQL `16.4.x`

#### 🗝️Server

- AWS EC2 (Ubuntu `20.04`)
- Nginx `1.23` (Reverse Proxy)
- Gunicorn `20.1.0` (WSGI Application Server)
- HTTPS (TLS `1.2`)

#### 🕹️IDE

- VSCode `1.69.2`
- InteliJ

## 🌟아키텍처
<img width="1000" alt="아키텍처" src="https://github.com/user-attachments/assets/831e383c-8ae0-4ae8-8a24-b84534cc5f61">

# 📂기획 및 설계 산출물

## 💭요구사항 정의 및 기능 명세([Notion](https://www.notion.so/ebb329f0e6f749e0947046f1dfa628d8?v=fd2c8b8ab04d4e06a10654310a2e4638)) - 일부 캡쳐
<img src="https://github.com/user-attachments/assets/d1b4a673-c1ba-464f-995b-f03fb4f9d8bb" alt="기능 명세서" width="1000"  height="400">

## 🎨화면 설계([Figma](https://www.figma.com/design/GNy9zyW1y3IQk1oaukzBrK/PiroTime?node-id=70-4&t=HZbUcis6l2gl7siK-0))
<img src="https://github.com/user-attachments/assets/fa32a01d-544e-4454-96c5-82c6e9f06f42" alt="Figma" width="1000"  height="500">

## 📜[ERD](https://www.erdcloud.com/d/SEz3HouJH7wNG4B8W)
<img src="https://github.com/user-attachments/assets/7cddc4cd-f479-4f96-8635-e7dbe6b733da" alt="ERD" width="1000"  height="500">

# 💞팀원 소개

#### PiroTime을 개발한 피로그래밍 21기 팀원들을 소개합니다!

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/JuheeeKim">
        <img src="https://github.com/user-attachments/assets/8904c618-4873-40ec-ab9d-789d2c8f55db" width="250px;" alt="나"><br>
        <b>FE/BE 팀장: 김주희</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/YourLink1">
        <img src="https://github.com/user-attachments/assets/64d688b5-173e-4a3e-bcc8-5be6fe3f2a70" width="250px;" alt="수용빠"><br>
        <b>FE/BE 팀원: 이수용</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/nawkwoo">
        <img src="https://github.com/user-attachments/assets/ef2e635a-001d-4250-8bcc-6abe958be91d" width="250px;" alt="관우빠"><br>
        <b>FE/BE 팀원: 손관우</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/C2hazelnut">
        <img src="https://github.com/user-attachments/assets/188861f6-37dc-4d84-8857-a2de6882e38d" width="250px;" alt="연진"><br>
        <b>FE/BE 팀원: 이연진</b>
      </a>
    </td>
  </tr>
</table>

## 🥰팀원 역할
- 김주희
  - 회원가입/로그인, 커피챗, 회원관리
- 손관우
  - 리뷰 게시판, IT 동향 게시판, 마이페이지
- 이수용
  - 협업 게시판, 마이페이지, 메일 시스템 관리
- 이연진
  - 랜딩 페이지, 메인 페이지, 커피챗
