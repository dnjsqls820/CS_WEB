# users/choice.py

#choice 필드에서 사용되고 있는 CHOICES 들을 따로 관리하기 위해 users 앱 내부에 choice.py라는 파일을 생성함

GRADE_CHOICES = (
    ("선택안함", "선택안함"),
    ("1학년", "1학년"),
    ("2학년", "2학년"),
    ("3학년", "3학년"),
    ("4학년", "4학년"),
    ("졸업생", "졸업생")
)

LEVEL_CHOICES = (
    ("3", "Lv3_미인증사용자"),
    ("2", "Lv2_인증사용자"),
    ("1", "Lv1_관리자"),
    ("0", "Lv0_개발자"),
)

CIRCLES_CHOICES = (
    ("미가입", "미가입"),
    ("멀티미디어","멀티미디어"),
    ("CE랩","CE랩")
    
)

DEPARTMENT_CHOICES = (
    
)