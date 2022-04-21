# Django&Postgresql을 이용한 컴퓨터공학과 홈페이지 만들기

## 1. 목적

개발기록 포스팅입니디. 프로젝트를 진행하면서 공부한 내용과 개발한 과정을 기록해 나중에 까먹지 않도록 남길것입니다.

Django에 대해 자세히 알진 못하기에 구현과정 중 틀린 부분 또는 Django Convention을 지키지 않았을 수도 있습니다.

## 2. 개발스택

> - Backend : Django/python
> - Frontend : Javascript, jQuery, Bootstarp4
> - DB : Postgresql
> - 서버 : Ubuntu 18.04, Nginx
> - 버전관리 : Git

## 3. 개발환경

> - OS : Ubuntu 18.04
> - IDE : VsCode
> - Python : 3.6.9
> - Django : *2.0.13*
> - Postgresql : *10.19*

## 4. 프로젝트 소개

Django CRUD를 공부하면서 공부한 내용에 추가하고 싶은 기능을 추가하여 Django에 대해 공부하고 학과에서 사용할 수 있는 Django 프레임워크 기반의 학과 랩실 홈페이지 프로젝트입니다.

## 5. 프로젝트 기능

![01](https://parkhyeonchae.github.io/2020/03/22/django-project-01/01.PNG)

- users

  > 사용자 계정 App입니다. 기본적인 로그인, 회원가입, SMTP를 활용한 인증, 프로필수정, Ajax로 ID/PW 찾기, PW변경, 회원탈퇴 등의 기능을 구현했습니다.

- notice

  > 공지사항 App입니다. 관리자 권한의 계정만 CRUD가 가능하며 게시글 검색, 공지사항 상단표시 등과 같은 기능을 추가했습니다.

- free

  > 자유게시판 App입니다. 질문, 정보와 같은 카테고리를 추가하였고, 공지사항 App과 달리 Ajax로 댓글달기. 답글달기와 같은 기능을 추가했습니다.

- anonymous

  > 익명게시판 App입니다. 에브리타임을 모티브로 한 무한스크롤형식의 게시판입니다. 작성자는 익명으로 표시되며 추천하기 등의 기능을 추가했습니다.

- calender

  > 학과일정 App입니다. Django Model만 연결했으며 JavaScript로 구현했습니다.

- timetable

  > 학과시험시간표 App입니다. 학년별 시험시간표, 사용자가 수강하는 과목만 선택하여 테이블형식으로 시험시간표를 볼수 있습니다. 관리자 권한의 사용자는 시험시간표를 업데이트 할 수 있으며, 마지막 업데이트 시간을 표시하게 구현했습니다.

- about

  > 학생회 정보, 학과 내 연구실 소개 등과 같은 기능을 추가한 App입니다.