from typing import Any



def deserialize(data: dict, serializer: Any) -> dict:
    serializer_obj = serializer(data=data)
    serializer_obj.is_valid(raise_exception=True)
    return serializer_obj.validated_data

#
# data_serializer = ActionStatusSerializer(data=request.data)
# data_serializer.is_valid(raise_exception=True)
# status = data_serializer.validated_data['action']
# status=deserialize(data=request.data,serializer=ActionStatusSerializer)