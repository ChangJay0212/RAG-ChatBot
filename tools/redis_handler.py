import json
import os

import redis


class RedisNotifier:
    def __init__(
        self,
        host: str = "redis",
        port: int = 6379,
        password: str = "admin",
        keyword: str = "span_id",
    ):
        self.host = host
        self.port = port
        self.password = password
        # self.db_id = db_id
        self.keyword = keyword
        self.cursor = self._connect()

    def _connect(self):
        """
        Connect to redis.
        """
        cursor = redis.Redis(host=self.host, port=self.port, password=self.password)
        return cursor

    def send(self, message: str):
        """
        Save message to redis.

        Args:
            message (str): Information.
        """
        self.cursor.set(self.keyword, message)
        # self.cursor.lpush(self.keyword, message)

        # print(message, flush=True)

    def get_value(self):
        """
        Get value from redis.

        Returns:
            redis: value from redis.
        """
        return self.cursor.get(self.keyword)

    def close(self):
        """
        Close connect.
        """
        self.cursor.close()


if __name__ == "__main__":
    message = 0.1
    redis_notifier = RedisNotifier()
    redis_notifier.send("7777")
    value = redis_notifier.get_value()
    print(value)
