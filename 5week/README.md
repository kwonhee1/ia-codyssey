# 요구 사항 분석하기

> 1. Computer Class 구현하기

반복 작업 worker 관리하는 class
run, stop, restart, exit 함수를 제공한다
worker 내부 stop_event를 사용하여 worker 를 조절한다

내부 변수
-   jobs : { id : {worker_thread, interval, execute_job, stop_event} } 형태로 실행 관리

함수

-   **init**()
-   run(execute executeJob, int interval) -\> int
    -   새로운 실행을 생성, 실행하고 id 반환
-   restart(job_id : int)
    -   해당 id의 실행을 시작
-   stop(job_id : int)
    -   해당 id의 실행을 종료
-   exit(job_id : int)
    -   해당 id의 thread, 메모리 정리

------------------------------------------------------------------------

> 2. MissionComputer Class 구현하기

한 개의 sensor를 가지며, computer를 상속받아 thread의 행동을 관리한다

내부 변수
-   private get_sensor_job_id : int :: computer의 thread id 값
-   private print_average_job_id : int
-   sensor : sensor 저장
-   history : 평균 계산을 위한 데이터 저장 리스트

함수
-   **init**(sensor, interval : int = 5) 
-   start_get_sensor(interval : int = 5) : computer에게 thread를 배정 받고 excute로 get_sensor_data 함수를 주고 실행함
-   start_print_average(interval : int = 300) : 5분 마다 history를 읽고 평균을 json으로 출력한다
-   get_sensor_data() -> void : 센서의 값을 읽고 history에 저장한다, json으로 변경하여 출력한다
-   read_sensor_data() -> dict
-   stop() : computer thread stop : 모든 thread 를 정리하고 모든 리소스를 정리한다
    -   [HH:MM:SS] [system] System stoped.... 형식으로 출력한다

------------------------------------------------------------------------

## 3. DummySensor 사용 방식 (기존 코드 유지)

------------------------------------------------------------------------

## 5. 실행 흐름

1.  dummy_stage.txt 파일 읽기\
2.  DummySensorStage 생성\
3.  DummySensor 생성\
4.  MissionComputer 생성\
5.  MissionComputer.start_get_sensor(), MissionComputer.start_print_average()
6.  while문을 돌면서 사용자가 Ctrl+c를 누르는지 확인하고 Ctrl + c를 누른 경우 MissionComputer.stop()

------------------------------------------------------------------------

## 제한 사항

-   python 3.x 사용
-   표준 라이브러리만 사용 (threading, time, json, random)
-   코드 스타일 준수
-   전체 코드를 mars_mission_computer.py 에 작성

------------------------------------------------------------------------

# class 정리

> Sensor : interface
get_env(), set_env() 를 가진다

> DummySensor
화성 기지 내부 / 외부 상태값들을 저장한다
__init__(stage : DummySensorStage, log_file : str = '')
set_env() : env_values 사전 객체를 랜덤 값으로 초기화한다
get_env() -> dict : env_values 값을 반환하며 log_env()를 호출한다
log_env() : env_values 값들을 파일에 로그로 남긴다 (보너스 과제)

> DummySensorStage
DummySensor의 random 값들의 범위를 책임지는 class
DEFAULT_MIN = 0, DEFAULT_MAX = 100 (파싱 실패 시 기본값)
__init__(lines : list) : 문자열 리스트를 파싱하여 센서별 범위를 설정한다
내부에서 {'sensorName': (min, max), ... } dict 형식
static cast_value(range_tuple : tuple) -> tuple : 문자열 튜플을 int/float로 캐스팅
get_ranges() -> dict : 센서별 범위 사전을 반환한다

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
dict을 json(String)으로 변환해주고 출력하는 class
static to_json(dict dict) -> string

> Computer
내부 변수
-   jobs : { id : {worker_thread, interval, execute_job, stop_event} } 형태로 실행 관리

함수

-   **init**()
-   run(execute executeJob, int interval) -\> int
    -   새로운 실행을 생성, 실행하고 id 반환
    -   exceuteJob : 반복 실행할 콜백 함수 (매겨 변수 없음)
-   restart(job_id : int)
    -   해당 id의 실행을 시작
-   stop(job_id : int)
    -   해당 id의 실행을 종료
-   exit(job_id : int)
    -   해당 id의 thread, 메모리 정리

> MissionComputer
내부 변수
-   private get_sensor_job_id : int :: computer의 thread id 값
-   private print_average_job_id : int
-   sensor : sensor 저장
-   history : 평균 계산을 위한 데이터 저장 리스트

함수
-   **init**(sensor, interval : int = 5) 
-   start_get_sensor(interval : int = 5) : computer에게 thread를 배정 받고 excute로 get_sensor_data 함수를 주고 실행함
-   start_print_average(interval : int = 300) : 5분 마다 history를 읽고 평균을 json으로 출력한다
-   get_sensor_data() -> void : 센서의 값을 읽고 history에 저장한다, json으로 변경하여 출력한다
-   read_sensor_data() -> dict
-   stop() : computer thread stop : get_sensor, print_average thread 를 정리하고 모든 리소스를 정리한다
    -   [HH:MM:SS] [system] System stoped.... 형식으로 출력한다

