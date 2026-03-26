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

class Substance(Element):
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        return value.strip().lower() == 'substance'

    @classmethod
    def of(cls, value: str):
        return cls(value.strip())

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.value


class Weight(Element):
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        # 'Weight (g/cm³)'와 같이 단위가 포함된 경우 처리
        return 'weight' in value.strip().lower()

    @classmethod
    def of(cls, value: str):
        return cls(value.strip())

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.value


class SpecificGravity(Element):
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        return value.strip().lower() == 'specific gravity'

    @classmethod
    def of(cls, value: str):
        return cls(value.strip())

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.value


class Strength(Element):
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        return value.strip().lower() == 'strength'

    @classmethod
    def of(cls, value: str):
        return cls(value.strip())

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.value


class Flammability(Element):
    def __init__(self, value: float):
        self.value = value

    @classmethod
    def is_match(cls, value: str) -> bool:
        return value.strip().lower() == 'flammability'

    @classmethod
    def of(cls, value: str):
        # 숫자로 변환하여 저장
        return cls(float(value.strip()))

    def __lt__(self, other) -> bool:
        if not isinstance(other, Flammability):
            return NotImplemented
        return self.value < other.value

    def __repr__(self) -> str:
        return str(self.value)

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
        return f"{', '.join(repr(e) for e in self._elements)}"


class BinneryMapper:
    @staticmethod
    def binneryEncoder(text: str) -> str:
        if not text:
            return ""
        return ' '.join(format(ord(char), '08b') for char in text)

    @staticmethod
    def binneryDecoder(binary_str: str) -> str:
        if not binary_str:
            return ""
        try:
            return ''.join(chr(int(b, 2)) for b in binary_str.split(' '))
        except ValueError:
            return ""

class FileReader:
    @staticmethod
    def read(filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return '\n'.join(line.strip() for line in lines if line.strip())
        except FileNotFoundError:
            print(f'파일을 찾을 수 없습니다: {filepath}')
            return ""
        except Exception as e:
            print(f'오류 발생: {e}')
            return ""


class FileWriter:
    @staticmethod
    def write(filepath: str, data: str):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception as e:
            print(f'오류 발생: {e}')


class Storage:
    """Data(Element 모음)를 전문으로 관리하는 클래스"""

    def __init__(self, initial_data: list = None):
        if initial_data is None:
            self._data = []
        else:
            self._data = initial_data

    def __repr__(self) -> str:
        return '\n'.join(str(data) for data in self._data)

    def set(self, data):
        self._data = data

    def add(self, data):
        self._data.append(data)

    def for_each(self, action):
        for data in self._data:
            action(data)

    def sort(self, key_cls, ascending: bool = True):
        """key_cls 기준으로 데이터를 정렬. ascending이 True면 오름차순, False면 내림차순"""
        
        self._data.sort(key=lambda data: data.get(key_cls), reverse=not ascending)

    def filter(self, condition):
        return Storage([data for data in self._data if condition(data)])


class Main:
    def __init__(self):
        self.storage = Storage()

    def run(self, filepath: str, error_filepath: str):
        print(FileReader.read(filepath))
        lines = FileReader.read(filepath).split('\n')

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

        print("------print all -------")
        print(str(self.storage))
        self.storage.for_each(print)
        
        self.storage.sort(Flammability, ascending=False)
        filteredStorage = self.storage.filter(lambda d: d.get(Flammability).value >= 0.7)

        print("------sort and filterd ------------- ")
        filteredStorage.for_each(print)

        FileWriter.write(error_filepath, str(filteredStorage))

        print("----binnery -------- ")
        FileWriter.write('Mars_Base_Inventory_danger.bin', BinneryMapper.binneryEncoder(str(self.storage)))
        print(BinneryMapper.binneryDecoder(FileReader.read('Mars_Base_Inventory_danger.bin')))

if __name__ == '__main__':
    Main().run('Mars_Base_Inventory_List.csv', 'Mars_Base_Inventory_danger.csv')
