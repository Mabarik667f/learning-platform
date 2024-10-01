class BaseTestClass:
    prefix = ""

    @classmethod
    def get_endpoint(cls, url: str | int) -> str:
        return f"{cls.prefix}/{url}"
