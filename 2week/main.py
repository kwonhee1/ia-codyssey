class Element:
    """각각의 요소를 담당하는 인터페이스"""
    
    _element_classes = []

    @classmethod
    def __init_subclass__(cls):
        Element._element_classes.append(cls)

    @staticmethod
    def find_element_type(value: str):
        """배열을 순회하며 매칭되는 하위 Element 클래스를 반환합니다."""
        for el_cls in Element._element_classes:
            if el_cls.is_match(value):
                return el_cls
        raise ValueError(f'지원하지 않는 Element Type 입니다: {value}')

    @classmethod
    def is_match(cls, value: str) -> bool:
        """문자열이 해당 Element의 타입인지 확인"""
        raise NotImplementedError('하위 클래스에서 구현되어야 합니다.')

    @classmethod
    def of(cls, value: str):
        """문자열로부터 Element를 생성하는 팩토리 메서드"""
        raise NotImplementedError('하위 클래스에서 구현되어야 합니다.')

    def __lt__(self, other) -> bool:
        """정렬(sort)을 위한 비교 메서드"""
        raise NotImplementedError('하위 클래스에서 구현되어야 합니다.')


class Timestamp(Element):
    """Timestamp를 담당하는 Element"""

    def __init__(self, value: str):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        return value.strip().lower() == 'timestamp'

    @classmethod
    def of(cls, value: str):
        return cls(value.strip())

    def __lt__(self, other) -> bool:
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self.value < other.value

    def __repr__(self) -> str:
        return f"{self.value}"


class Event(Element):
    """Event를 담당하는 Element"""

    def __init__(self, value: str):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        return value.strip().lower() == 'event'

    @classmethod
    def of(cls, value: str):
        return cls(value.strip())

    def __lt__(self, other) -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        return self.value < other.value

    def __repr__(self) -> str:
        return f"{self.value}"


class Message(Element):
    """Message를 담당하는 Element"""

    def __init__(self, value: str):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        return value.strip().lower() == 'message'

    @classmethod
    def of(cls, value: str):
        return cls(value.strip())

    def __lt__(self, other) -> bool:
        if not isinstance(other, Message):
            return NotImplemented
        return self.value < other.value

    def __repr__(self) -> str:
        return f"{self.value}"


class Data:
    """로그 한 줄을 파싱하여 저장하는 entity 클래스 (여러 개의 Element를 가짐)"""

    def __init__(self, elements):
        self._elements = elements

    def get(self, element_cls):
        """특정 Element 클래스(타입)에 해당하는 요소를 찾아 반환"""
        for el in self._elements:
            if isinstance(el, element_cls):
                return el
        return None

    def __repr__(self) -> str:
        return f"Data({', '.join(repr(e) for e in self._elements)})"


class FileReader:
    """파일을 읽어 list[str]로 반환하는 static 클래스"""

    @staticmethod
    def read(filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [line.strip() for line in lines if line.strip()]
        except FileNotFoundError:
            print(f'파일을 찾을 수 없습니다: {filepath}')
            return []
        except Exception as e:
            print(f'오류 발생: {e}')
            return []


class FileWriter:

    @staticmethod
    def write(filepath: str, data_list: list):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for data in data_list:
                    line = ','.join(el.value for el in data._elements)
                    f.write(line + '\n')
        except Exception as e:
            print(f'오류 발생: {e}')


class Storage:
    """Data(Element 모음)를 전문으로 관리하는 클래스"""

    def __init__(self):
        self._data = []

    def set(self, data):
        self._data = data

    def get(self):
        return self._data

    def sort(self, key_cls, ascending: bool = True):
        """key_cls 기준으로 데이터를 정렬. ascending이 True면 오름차순, False면 내림차순"""
        
        self._data.sort(key=lambda data: data.get(key_cls), reverse=not ascending)

    def filter(self, condition):
        return [data for data in self._data if condition(data)]


class Main:
    """FileReader와 Storage를 조합하여 실행 흐름 제어"""

    def __init__(self):
        self.storage = Storage()

    def run(self, filepath: str, error_filepath: str):
        lines = FileReader.read(filepath)
        if not lines:
            print('읽을 데이터가 없습니다.')
            return

        header = lines[0]
        # Element 클래스에 새로 만든 함수를 통해 헤더의 각 컬럼에 맞는 구체 클래스를 찾아 배열로 구성합니다.
        element_classes = [Element.find_element_type(col) for col in header.split(',')]

        data_list = []
        for line in lines[1:]:
            values = line.split(',', len(element_classes) - 1)
            
            elements = [
                cls.of(val) 
                for cls, val in zip(element_classes, values)
            ]
            data_list.append(Data(elements))

        self.storage.set(data_list)
        self.storage.sort(Timestamp, False)

        for data in self.storage.get():
            print(data)

        errors = self.storage.filter(lambda d: d.get(Event).value == 'ERROR')
        FileWriter.write(error_filepath, errors)


if __name__ == '__main__':
    Main().run('mission_computer_main.log', 'error.log')
