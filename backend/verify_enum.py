from enum import Enum

class FeatureType(str, Enum):
    chat = "chat"

def test_func(ft):
    print(f"Type: {type(ft)}")
    print(f"Value: {ft.value}")

if __name__ == "__main__":
    print("Testing Enum behavior")
    try:
        test_func(FeatureType.chat)
        print("Success")
    except Exception as e:
        print(f"Failed: {e}")
