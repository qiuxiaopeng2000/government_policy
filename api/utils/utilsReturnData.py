from ..models import user_info_data, follow
from django.db.models import Q


def follow_users(cityName,categoryName):
    print("cityname" + cityName + '\ncategoryName:' + categoryName)
    querySet = follow.objects.filter(Q(follow_city = cityName) | Q(follow_category = categoryName)).all()
    userNameArray = []
    for i in querySet:
        userNameArray.append(i.username)
    return set(userNameArray)