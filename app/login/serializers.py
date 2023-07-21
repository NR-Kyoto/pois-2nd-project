'''
Author: dnimo kuochingcha@gmail.com
Date: 2023-07-03 16:01:32
LastEditors: dnimo kuochingcha@gmail.com
LastEditTime: 2023-07-04 18:10:59
FilePath: /pois-2nd-project/app/login/serializers.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)