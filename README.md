# KPA2023_jjy

# KSCBP2023_jjy
[한국심리학회] 프로그래밍 도구, 화면 재생 빈도, 운영체제에 따른 시각 자극 제시 정확도 비교
> 문의: word3276@gmail.com

---------------------------
**MATLAB R2022b & Psychtoolbox 3.0.19**

- 실행파일명: *KPA2023_PTB3_jjy.m*

- 절차: 실행 > 입력창에 파라미터 입력 > 'Press Z' 문구가 뜨면 z키(블록 1) > 자극 제시 후 스페이스바(16회 반복) > 'Press Z' 문구가 뜨면 z키(블록 2) > ... > 블록 15가 끝나면 자동 종료

- 프로그램 측정 데이터파일 경로: [result] 폴더

- 프로그램 측정 데이터파일 변인명: 1. ID  2. 블록번호  3. 시행번호  4. 운영체제  5. PC종류  6. 화면 재생 빈도(hz)
                                  7. 코드: while[1]/개발자[2] 8. 지연요소: 없음[0]/키입력직후[1]/반복문[2]
                                  9. 자극 제시시간(의도)  10. 자극 지속시간(프로그램)  11. 검은화면 제시시간(프로그램)


---------------------------
**PsychoPy 2023.1.3 & Python 3.8**

- 실행파일명: *PsychoPy_coder.py*

- 절차: 실행 > 입력창에 파라미터 입력 > 'Press Z' 문구가 뜨면 z키(블록 1) > 자극 제시 후 스페이스바(16회 반복) > 'Press Z' 문구가 뜨면 z키(블록 2) > ... > 블록 15가 끝나면 자동 종료

- 프로그램 측정 데이터파일 경로: [result] 폴더

- 프로그램 측정 데이터파일 변인명: 1. ID  2. 블록번호  3. 시행번호  4. 운영체제  5. PC종류  6. 화면 재생 빈도(hz)
                                  7. 코드: while[1]/개발자[2] 8. 지연요소: 없음[0]/키입력직후[1]/반복문[2]
                                  9. 자극 제시시간(의도)  10. 자극 지속시간(프로그램)  11. 검은화면 제시시간(프로그램)


---------------------------
**E-Prime 3.0.3.214**

- 실행파일명: *KPA2023_Eprime3_jjy.es3*

- 절차: 실행 > 파라미터 선택 > 'Press Z' 문구가 뜨면 z키(블록 1) > 자극 제시 후 스페이스바(16회 반복) > 'Press Z' 문구가 뜨면 z키(블록 2) > ... > 블록 15가 끝나면 자동 종료

- 프로그램 측정 데이터파일 경로: 프로그램 실행 후 직접 지정

- 프로그램 측정 데이터파일 변인명: ptime[자극 제시시간] target.Duration[자극 지속시간(프로그램)] target.DurationError[자극 지속시간 오차(프로그램)]
  
  * 발표 포스터에서 '프로그램에 기록된 자극 제시시간 오류'는 *target.Duration + target.DurationError* 로 계산되었음.


---------------------------
**SuperLab 6.3.1**

- 실행파일명: *KPA2023_Superlab6_jjy.sl6*

- 절차: 실행 >  파라미터 선택 > 'Press Z' 문구가 뜨면 z키(블록 1) > 자극 제시 후 스페이스바(16회 반복) > 'Press Z' 문구가 뜨면 z키(블록 2) > ... > 블록 15가 끝나면 자동 종료

- 프로그램 측정 데이터파일 경로: 프로그램 실행 후 직접 지정

- 프로그램 측정 데이터파일 변인명: Event Name[이벤트(자극) 이름] target_t[자극 지속시간(프로그램)]
