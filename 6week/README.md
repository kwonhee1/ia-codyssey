# 요구 사항 분석하기

> ComputerStage class 구현
생성자 : ComputerStage(self, setting : str)

함수
- info() -> dict
- load() -> dict

> Computer class 함수 추가
- get_computer_info() 함수 추가
1. 운영체계
2. 운영체계 버전
3. CPU의 타입
4. CPU의 코어 수
5. 메모리의 크기
5개 정보 dict 반환

- get_computer_load() 함수 추가
1. CPU 실시간 사용량
2. 메모리 실시간 사용량
2개 정보 dict 반환

> MissionComputer class 함수 추가

- get_mission_computer_info() 추가
- get_mission_computer_load() 추가
super class의 함수 dict을 json으로 print 출력 (json mapper 사용)

------------------------------------------------------------------------

## 5. 실행 흐름

1.  dummy_stage.txt 파일 읽기\
1.  computer_stage.txt 파일 읽기, ComputerStage class 생성\
2.  DummySensorStage 생성\
3.  DummySensor 생성\
4.  MissionComputer 생성\
5.  MissionComputer.get_mission_computer_info(), MissionComputer.get_mission_computer_load()
5.  MissionComputer.start_get_sensor(), MissionComputer.start_print_average()
6.  while문을 돌면서 사용자가 Ctrl+c를 누르는지 확인하고 Ctrl + c를 누른 경우 MissionComputer.stop()

------------------------------------------------------------------------

# 제한 사항

-   python 3.x 사용
-   표준 라이브러리만 사용 (threading, time, json, random, platform, os, ctypes)
-   코드 스타일 준수
-   전체 코드를 mars_mission_computer.py 에 작성

------------------------------------------------------------------------

# class 정리

> Sensor : interface
get_env(), set_env() 를 가진다

> DummySensor
화성 기지 내부 / 외부 상태값들을 저장한다
__init__(self, stage : DummySensorStage, log_file : str = '')
set_env() : env_values 사전 객체를 랜덤 값으로 초기화한다
get_env() -> dict : env_values 값을 반환하며 log_env()를 호출한다
log_env() : env_values 값들을 파일에 로그로 남긴다 (보너스 과제)

> DummySensorStage
DummySensor의 random 값들의 범위를 책임지는 class
DEFAULT_MIN = 0, DEFAULT_MAX = 100 (파싱 실패 시 기본값)
__init__(self, lines : list) : 문자열 리스트를 파싱하여 센서별 범위를 설정한다
내부에서 {'sensorName': (min, max), ... } dict 형식
cast_value(self, range_tuple : tuple) -> tuple : 문자열 튜플을 int/float로 캐스팅
get_ranges(self) -> dict : 센서별 범위 사전을 반환한다

> Random
random 값을 발생시키기 위한 class
static random_float(include_min : float, include_max : float) -> float
static random_int(include_min : int, include_max : int) -> int
static random(a, b) : a, b 타입에 따라 적절한 랜덤 값을 반환한다

> FileReader
파일을 읽는 class
static read(file : str) -> str (FileNotFoundError, PermissionError 처리 포함)

> FileWriter
파일을 쓰는 class
static write(file : str, content : str)

> JsonMapper
dict을 json(String)으로 변환해주는 class
static to_json(dict_obj : dict) -> str

> Computer
내부 변수
-   jobs : { id : {worker_thread, interval, execute_job, stop_event} } 형태로 실행 관리
-   computer_stage : ComputerStage 인스턴스

함수

-   __init__(self, stage : ComputerStage = None)
-   run(self, execute_job, interval : int) -> int
    -   새로운 실행을 생성, 실행하고 id 반환
    -   execute_job : 반복 실행할 콜백 함수 (매개변수 없음)
-   restart(self, job_id : int)
    -   해당 id의 실행을 시작
-   stop(self, job_id : int)
    -   해당 id의 실행을 종료
-   exit(self, job_id : int)
    -   해당 id의 thread, 메모리 정리
-   get_computer_info(self) -> dict
    -   computer의 정보 운영체계, 운영체계 버전, CPU의 타입, CPU의 코어 수, 메모리의 크기를 dict으로 반환함
-   get_computer_load(self) -> dict
    -   computer 정보 CPU 실시간 사용량, 메모리 실시간 사용량을 dict으로 반환함

> MissionComputer
내부 변수
-   private get_sensor_job_id : int :: computer의 thread id 값
-   private print_average_job_id : int
-   sensor : sensor 저장
-   history : 평균 계산을 위한 데이터 저장 리스트

함수
-   __init__(self, sensor : Sensor, stage : ComputerStage = None, interval : int = 5)
-   start_get_sensor(self, interval : int = 5) : computer에게 thread를 배정 받고 execute로 get_sensor_data 함수를 주고 실행함
-   start_print_average(self, interval : int = 300) : 5분 마다 history를 읽고 평균을 json으로 출력한다
-   get_sensor_data(self) : 센서의 값을 읽고 history에 저장한다, json으로 변경하여 출력한다
-   read_sensor_data(self) -> dict
-   stop(self) : get_sensor, print_average thread를 정리하고 모든 리소스를 정리한다
    -   [HH:MM:SS] [system] System stoped.... 형식으로 출력한다
-   get_mission_computer_info(self) : computer info를 json으로 출력함
-   get_mission_computer_load(self) : computer load를 json으로 출력함

> ComputerStage
Computer의 시스템 정보와 실시간 부하를 수집하는 class

내부 변수
-   setting : 설정 파일 경로
-   _setting_data : 설정 파일에서 파싱한 key=value 데이터

함수
-   __init__(self, setting : str = '')
-   info(self) -> dict : 운영체계, 운영체계 버전, CPU의 타입, CPU의 코어 수, 메모리의 크기를 반환
-   load(self) -> dict : CPU 실시간 사용량, 메모리 실시간 사용량을 반환
-   _get_total_memory(self) -> int : 시스템 전체 메모리 바이트를 반환
-   _get_memory_usage(self) -> float : 메모리 사용률(%)을 반환
-   _get_cpu_usage(self) -> float : CPU 사용률(%)을 반환
