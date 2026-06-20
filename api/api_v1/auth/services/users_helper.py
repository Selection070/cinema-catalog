from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """
    - Получение пароля юзера
    - Проверка переданного пароля
    """

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """
        Получение пароля юзернейма если есть
        :param username:
        :return:
        """

    @classmethod
    def check_password_match(cls, password_db: str, password_in: str) -> bool:
        return password_db == password_in

    def validate_user_password(self, username: str, password: str) -> bool:
        db_password = self.get_user_password(username)

        if db_password is None:
            return False

        return self.check_password_match(db_password, password)
