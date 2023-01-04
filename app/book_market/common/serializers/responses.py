from rest_framework.serializers import BaseSerializer
from typing import Self


class SuccessResponseSerializer(BaseSerializer):
    def __init__(self: Self, result: bool):
        self.result = result

    @property
    def data(self: Self):
        return {
            "success": self.result
        }
