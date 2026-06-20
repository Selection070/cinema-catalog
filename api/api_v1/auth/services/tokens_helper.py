from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    """
    - Check tokens
    -Save tokens
    -Add tokens
    """

    @abstractmethod
    def check_token(self, token: str) -> bool:
        """
        Check is token exists
        :param token:
        :return:
        """

    @abstractmethod
    def save_token(self, token: str) -> None:
        """
        Save toke in storage
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Add token in storage
        :param token:
        :return:
        """
