# 천명기어 한글화 프로젝트
본 프로젝트의 목적은 천명기어1편을 한글화하는 것입니다.. 네이버 카페 소요객잔(https://cafe.naver.com/beemu) 후원으로 시작되었습니다.

## 프로젝트 환경설정
```bash
pip install -r requirements.txt
# 만약 openai를 번역 백엔드로 사용할 경우 openai, titoken을 추가 설치
pip install openai titoken
```
## 프로젝트 구조
/build/ : 최종적으로 패치가 완료된 결과물

/data/ : 게임과 관련된 각 데이터들이 들어있는 폴더

/gulongpatcher : 고룡풍운록 번역에 사용할 파이썬 패키지

/sampleconfig.toml : 패치 구동환경에 따른 로컬 설정 샘플

## 패치 방식
1. 천명기어 내부 텍스트 추출
2. AI를 이용해 텍스트 변환 테이블 제작
3. 2번 데이터의 id,텍스트를 기준으로 게임 내 텍스트 교체

config 파일을 교체하면 게임 내 텍스트가 한글로 출력됩니다.


## 추가로 구현이 필요한 부분
폰트 삽입 방법 찾아볼 것

## 번역 정보
이번 번역부터는 클로드만 사용할 예정입니다.

## 천명기어1의 데이터 구조
- 천명기어는 Asset폴더내의 movie_other와 textfiles 두개 파일에 모든 텍스트가 들어있음
- 기존 수작업으로 한 한글화 자료가 있으니 참조하여 작업 진행


코드 내에는 번역할 텍스트 정의가 포함되어 있습니다. 
```Python
Excel file 참조
```

# Special Thanks
소요객잔(https://cafe.naver.com/beemu) 대협들의 지원을 받았습니다.

무명대협들께서 지원해주신 금액은 모두 번역의 퀄리티를 향상시키기 위해 사용될 것입니다.