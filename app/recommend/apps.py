'''
Author: dnimo kuochingcha@gmail.com
Date: 2023-06-20 13:18:21
LastEditors: dnimo kuochingcha@gmail.com
LastEditTime: 2023-07-04 22:53:49
FilePath: /pois-2nd-project/app/recommend/apps.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.apps import AppConfig


class RecommendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.recommend'
