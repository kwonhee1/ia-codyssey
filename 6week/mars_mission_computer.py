import json
import os
import platform
import random as _random
import threading
import time


class Sensor:
    '''센서 인터페이스'''

    def get_env(self) -> dict:
        raise NotImplementedError('get_env() must be implemented')

    def set_env(self):
        raise NotImplementedError('set_env() must be implemented')


class Random:
    '''random 값을 생성하기 위한 클래스'''

    @staticmethod
    def random_float(include_min: float, include_max: float) -> float:
        '''include_min 이상 include_max 이하의 실수를 반환한다'''
        return round(_random.uniform(include_min, include_max), 2)

    @staticmethod
    def random_int(include_min: int, include_max: int) -> int:
        '''include_min 이상 include_max 이하의 정수를 반환한다'''
        return _random.randint(include_min, include_max)

    @staticmethod
    def random(a, b):
        '''입력 타입에 맞는 random 값을 반환한다'''
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError(
                f'Illegal Type {type(a).__name__}, {type(b).__name__}'
            )
        if isinstance(a, int) and isinstance(b, int):
            return Random.random_int(a, b)
        return Random.random_float(float(a), float(b))


class FileReader:
    '''파일을 읽는 클래스'''

    @staticmethod
    def read(file: str) -> str:
        '''파일을 읽어 문자열로 반환한다'''
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            print(f'파일을 찾을 수 없습니다: {file}')
            return ''
        except PermissionError:
            print(f'파일 읽기 권한이 없습니다: {file}')
            return ''


class FileWriter:
    '''파일을 쓰는 클래스'''

    @staticmethod
    def write(file: str, content: str):
        '''파일에 문자열을 쓴다'''
        try:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
        except PermissionError:
            print(f'파일 쓰기 권한이 없습니다: {file}')
        except OSError as e:
            print(f'파일 쓰기 오류: {e}')


class JsonMapper:
    '''dict를 json 문자열로 변환하는 클래스'''

    @staticmethod
    def to_json(dict_obj: dict) -> str:
        '''dict를 json 문자열로 반환한다'''
        return json.dumps(dict_obj, ensure_ascii=False)


class ComputerStage:
    '''Computer의 시스템 정보와 실시간 부하를 수집하는 클래스'''

    def __init__(self, setting: str = ''):
        '''setting 파일 경로를 받아 초기화한다'''
        self.setting = setting
        self._setting_data = {}
        if setting:
            content = FileReader.read(setting)
            if content:
                for line in content.splitlines():
                    line = line.strip()
                    if not line or '=' not in line:
                        continue
                    key, _, value = line.partition('=')
                    self._setting_data[key.strip()] = value.strip()

    def info(self) -> dict:
        '''운영체계, 버전, CPU 타입, CPU 코어 수, 메모리 크기를 반환한다'''
        memory_bytes = self._get_total_memory()
        memory_gb = round(memory_bytes / (1024 ** 3), 2) if memory_bytes else 'unknown'
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'cpu_type': platform.processor(),
            'cpu_cores': os.cpu_count(),
            'memory_size_gb': memory_gb,
        }

    def load(self) -> dict:
        '''CPU 실시간 사용량, 메모리 실시간 사용량을 반환한다'''
        cpu_usage = self._get_cpu_usage()
        memory_usage = self._get_memory_usage()
        return {
            'cpu_usage_percent': cpu_usage,
            'memory_usage_percent': memory_usage,
        }

    def _get_total_memory(self) -> int:
        '''시스템 전체 메모리 바이트를 반환한다'''
        try:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return stat.ullTotalPhys
        except Exception:
            pass
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal'):
                        return int(line.split()[1]) * 1024
        except Exception:
            pass
        return 0

    def _get_memory_usage(self) -> float:
        '''메모리 사용률(%)을 반환한다'''
        try:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return float(stat.dwMemoryLoad)
        except Exception:
            pass
        try:
            with open('/proc/meminfo', 'r') as f:
                info = {}
                for line in f:
                    parts = line.split()
                    if parts[0] in ('MemTotal:', 'MemAvailable:'):
                        info[parts[0]] = int(parts[1])
                total = info.get('MemTotal:', 0)
                avail = info.get('MemAvailable:', 0)
                if total > 0:
                    return round((total - avail) / total * 100, 2)
        except Exception:
            pass
        return 0.0

    def _get_cpu_usage(self) -> float:
        '''CPU 사용률(%)을 간이 측정하여 반환한다'''
        try:
            with open('/proc/stat', 'r') as f:
                line1 = f.readline()
            fields1 = [int(x) for x in line1.split()[1:]]
            time.sleep(0.1)
            with open('/proc/stat', 'r') as f:
                line2 = f.readline()
            fields2 = [int(x) for x in line2.split()[1:]]
            idle1, idle2 = fields1[3], fields2[3]
            total1, total2 = sum(fields1), sum(fields2)
            diff_total = total2 - total1
            diff_idle = idle2 - idle1
            if diff_total == 0:
                return 0.0
            return round((1 - diff_idle / diff_total) * 100, 2)
        except Exception:
            pass
        try:
            import subprocess
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'LoadPercentage', '/value'],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.splitlines():
                if 'LoadPercentage' in line:
                    return float(line.split('=')[1].strip())
        except Exception:
            pass
        return 0.0


class DummySensorStage:
    '''DummySensor가 사용할 랜덤 범위를 관리하는 클래스'''

    DEFAULT_MIN = 0
    DEFAULT_MAX = 100

    def __init__(self, lines: list):
        '''문자열 리스트를 파싱해 센서별 범위를 저장한다'''
        self.ranges = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            name = parts[0]
            try:
                self.ranges[name] = self.cast_value((parts[1], parts[2]))
            except (IndexError, TypeError):
                self.ranges[name] = (
                    DummySensorStage.DEFAULT_MIN,
                    DummySensorStage.DEFAULT_MAX,
                )

    def cast_value(self, range_tuple: tuple) -> tuple:
        '''문자열 튜플을 int 또는 float 튜플로 변환한다'''
        min_str, max_str = range_tuple[0], range_tuple[1]
        try:
            return (int(min_str), int(max_str))
        except ValueError:
            pass
        try:
            return (float(min_str), float(max_str))
        except ValueError as e:
            raise TypeError(
                f'Illegal Type {min_str}, {max_str}'
            ) from e

    def get_ranges(self) -> dict:
        '''센서별 범위를 반환한다'''
        return self.ranges


class DummySensor(Sensor):
    '''화성 기지의 환경값을 관리하는 센서'''

    def __init__(self, stage: DummySensorStage, log_file: str = ''):
        '''DummySensorStage를 받아 초기화한다'''
        self.stage = stage
        self.log_file = log_file
        self.env_values = {}

    def set_env(self):
        '''env_values를 랜덤 값으로 갱신한다'''
        ranges = self.stage.get_ranges()
        for name, (min_val, max_val) in ranges.items():
            self.env_values[name] = Random.random(min_val, max_val)

    def get_env(self) -> dict:
        '''env_values를 반환하고 필요하면 로그를 남긴다'''
        self.log_env()
        return dict(self.env_values)

    def log_env(self):
        '''env_values를 로그 파일에 저장한다'''
        if not self.log_file:
            return
        lines = []
        for name, value in self.env_values.items():
            lines.append(f'{name}: {value}')
        content = '\n'.join(lines)
        FileWriter.write(self.log_file, content)


class Computer:
    '''반복 작업을 worker thread로 관리하는 클래스'''

    def __init__(self, stage: ComputerStage = None):
        '''작업 저장소를 초기화한다'''
        self.jobs = {}
        self.next_job_id = 1
        self.computer_stage = stage or ComputerStage()

    def get_computer_info(self) -> dict:
        '''운영체계, 버전, CPU 타입, 코어 수, 메모리 크기를 반환한다'''
        return self.computer_stage.info()

    def get_computer_load(self) -> dict:
        '''CPU 실시간 사용량, 메모리 실시간 사용량을 반환한다'''
        return self.computer_stage.load()

    def run(self, execute_job, interval: int) -> int:
        '''새 작업을 시작하고 id를 반환한다'''
        job_id = self.next_job_id
        self.next_job_id += 1
        stop_event = threading.Event()
        worker_thread = self._create_worker(execute_job, interval, stop_event)
        self.jobs[job_id] = {
            'worker_thread': worker_thread,
            'interval': interval,
            'execute_job': execute_job,
            'stop_event': stop_event,
        }
        worker_thread.start()
        return job_id

    def _create_worker(
        self,
        execute_job,
        interval: int,
        stop_event: threading.Event,
    ) -> threading.Thread:
        '''반복 실행용 worker thread를 생성한다'''

        def worker():
            while not stop_event.is_set():
                execute_job()
                if stop_event.wait(interval):
                    break

        return threading.Thread(target=worker, daemon=True)

    def restart(self, job_id: int):
        '''정지된 작업을 다시 시작한다'''
        job = self.jobs.get(job_id)
        if not job:
            return
        worker_thread = job['worker_thread']
        if worker_thread.is_alive():
            return
        stop_event = threading.Event()
        worker_thread = self._create_worker(
            job['execute_job'],
            job['interval'],
            stop_event,
        )
        job['stop_event'] = stop_event
        job['worker_thread'] = worker_thread
        worker_thread.start()

    def stop(self, job_id: int):
        '''작업을 정지한다'''
        job = self.jobs.get(job_id)
        if not job:
            return
        job['stop_event'].set()
        job['worker_thread'].join(timeout=job['interval'] + 1)

    def exit(self, job_id: int):
        '''작업을 종료하고 저장소에서 제거한다'''
        if job_id not in self.jobs:
            return
        Computer.stop(self, job_id)
        del self.jobs[job_id]


class MissionComputer(Computer):
    '''센서 수집과 평균 출력을 관리하는 컴퓨터'''

    def __init__(self, sensor: Sensor, stage: ComputerStage = None, interval: int = 5):
        '''센서와 기본 수집 주기를 초기화한다'''
        super().__init__(stage)
        self.sensor = sensor
        self.sensor_interval = interval
        self.average_interval = 300
        self.average_started_at = None
        self.history = []
        self.get_sensor_job_id = None
        self.print_average_job_id = None

    def start_get_sensor(self, interval: int = 5):
        '''센서 수집 작업을 시작한다'''
        self.sensor_interval = interval
        if self.get_sensor_job_id is not None:
            self.exit(self.get_sensor_job_id)
        self.get_sensor_job_id = self.run(
            self.get_sensor_data,
            interval,
        )

    def start_print_average(self, interval: int = 300):
        '''평균 출력 작업을 시작한다'''
        self.average_interval = interval
        self.average_started_at = time.time()
        if self.print_average_job_id is not None:
            self.exit(self.print_average_job_id)
        self.print_average_job_id = self.run(
            self.print_average,
            interval,
        )

    def get_sensor_data(self):
        '''센서 값을 읽고 history에 저장한 뒤 json으로 출력한다'''
        data = self.read_sensor_data()
        self.history.append(data)
        self.print_with_time('sensor', JsonMapper.to_json(data))

    def read_sensor_data(self) -> dict:
        '''센서 값을 갱신하고 반환한다'''
        self.sensor.set_env()
        return self.sensor.get_env()

    def print_average(self):
        '''현재까지 수집한 평균값을 출력하고 history를 초기화한다'''
        if self.average_started_at is None:
            self.average_started_at = time.time()
        if time.time() - self.average_started_at < self.average_interval:
            return

        if not self.history:
            self.average_started_at = time.time()
            return
        snapshot = self.history[:]
        self.history = []

        averages = {}
        sensor_names = snapshot[0].keys()
        for name in sensor_names:
            total = 0
            for data in snapshot:
                total += data[name]
            averages[name] = round(total / len(snapshot), 2)
        self.average_started_at = time.time()
        self.print_with_time('average', JsonMapper.to_json(averages))

    def print_with_time(self, log_type: str, message: str):
        '''현재 시간을 포함해 메시지를 출력한다'''
        current_time = time.strftime('%H:%M:%S')
        print(f'[{current_time}] [{log_type}] {message}')

    def get_mission_computer_info(self):
        '''컴퓨터 정보를 JSON으로 출력한다'''
        info = self.get_computer_info()
        self.print_with_time('info', JsonMapper.to_json(info))

    def get_mission_computer_load(self):
        '''컴퓨터 부하 정보를 JSON으로 출력한다'''
        load = self.get_computer_load()
        self.print_with_time('load', JsonMapper.to_json(load))

    def stop(self):
        '''실행 중인 모든 작업을 정리한다'''
        if self.get_sensor_job_id is not None:
            Computer.exit(self, self.get_sensor_job_id)
            self.get_sensor_job_id = None
        if self.print_average_job_id is not None:
            Computer.exit(self, self.print_average_job_id)
            self.print_average_job_id = None
        self.print_with_time('system', 'System stoped....')


def main():
    '''미션 컴퓨터를 실행한다'''
    lines = FileReader.read('dummy_stage.txt').splitlines()
    dummy_stage = DummySensorStage(lines)
    sensor = DummySensor(dummy_stage, 'env_log.txt')
    computer_stage = ComputerStage('computer_stage.txt')
    mission_computer = MissionComputer(sensor, computer_stage)

    mission_computer.get_mission_computer_info()
    mission_computer.get_mission_computer_load()

    mission_computer.start_get_sensor()
    mission_computer.start_print_average()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mission_computer.stop()


if __name__ == '__main__':
    main()
