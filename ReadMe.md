# Django&Postgresql을 이용한 컴퓨터공학과 홈페이지 만들기

## 1. 목적

처음에 제가 속한 연구실의 홈페이지를 만들려고 기획하다 문득 우리 랩실 뿐만 아니라 다른 랩실도 사용할수 있는 홈페이지를 만들어 서로 정보를 공유하고 커뮤니케이션을 활성화 시키는 목적으로  이용자를 랩실 인원뿐만 아니라 컴퓨터공학과 학생들을 대상으로 사용할수 있는 cs_web을 구현했습니다.

## 2. 개발스택

> - Backend : Django/python
> - Frontend : Javascript, jQuery, Bootstarp4
> - DB : Postgresql
> - 버전관리 : Git

## 3. 개발환경

> - OS : Ubuntu 18.04
> - IDE : VsCode
> - Python : 3.6.9
> - Django : *2.0.13*
> - Postgresql : *10.19*

## 4. 프로젝트 소개

Django를 공부하면서 개인 프로젝트를 하고싶어 컴퓨터공학과 학생들을 대상으로 사용할수 있는 cs_web을 구연했습니다. 또한 instagram클론코딩을 하면서 배운 기술로 DDostagram이라는 인스타그램을 모티브로 한 앱을 만들고 Django에 대해 공부하면서 배운 내용들을 기반으로 기능을 구현한 학과에서 사용할 수 있는 cs_web 프로젝트입니다.

![](https://user-images.githubusercontent.com/75882110/174694536-c4639cb8-2638-441e-b2ee-9ef02dbc62a6.png)

![](https://user-images.githubusercontent.com/75882110/174694576-95562f58-3369-4bd5-aec8-689de64bfcb0.png)

## 5. 프로젝트 기능

![01](https://user-images.githubusercontent.com/75882110/174693228-8cedfdc7-2866-4955-80e6-87371d921c6e.png)

- users

  > 사용자 계정 App입니다. UserCreationForm을 기반으로 로그인, 회원가입, SMTP를 활용한 인증, 프로필수정, Ajax로 ID/PW 찾기, PW변경, 회원탈퇴 등의 기능을 구현했습니다.

- notice

  > ![](https://user-images.githubusercontent.com/75882110/174694402-777b4f98-0e7e-4b0a-9328-d5a3502ac2a6.png)
  >
  > 공지사항 App입니다. 관리자 권한의 계정만 CRUD가 가능하며 게시글 검색, 공지사항 상단표시 등과 같은 기능을 추가했습니다.

- free

  > ![](https://user-images.githubusercontent.com/75882110/174694376-00ad04d0-fb57-4b78-8fc3-a0a4a017a128.jpg)
  >
  > 자유게시판 App입니다. 질문, 정보와 같은 카테고리를 추가하였고, 공지사항 App과 달리 Ajax 비동기 형식 댓글달기. 답글달기와 같은 기능을 추가했습니다.

- Todo

  > ![](https://user-images.githubusercontent.com/75882110/174694331-5eb00e76-00ee-4a19-acb4-a3618f622594.jpg)
  >
  > 일정관리 앱입니다. 자신의 글만 보이게 구현했습니다.

- coocr

  > ![](https://user-images.githubusercontent.com/75882110/174694219-23f03525-e892-4fdc-8213-bd1a63cd35a6.jpg)
  >
  > Ocr모델을 사용해 이미지에 있는 텍스트를 추출해주는 페이지를 구현했습니다.

- user_admin

  > ![](https://user-images.githubusercontent.com/75882110/174694434-6f71ef0d-75a1-40a3-9ce7-898d8c497d4c.png)
  >
  > ![](https://user-images.githubusercontent.com/75882110/174694457-361d1e23-d485-42da-ad65-47bd04b29b16.png)
  >
  > 관리자, 개발자 레벨의 사용자만 해당 탭이 보이고 회원목록들을 나열하고 탈퇴시킬수 있게 구현했습니다.

- instagram

  > ![](https://user-images.githubusercontent.com/75882110/174694478-a5b2c6d5-5468-4cd0-a8e2-e52d6ba78a4c.jpg)
  >
  > SummerNote기반의 게시글 작성으로 인스타그램을 모티브로한 DDostagram을 구현했습니다.