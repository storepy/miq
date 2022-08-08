import json
import datetime
from django.utils.dateparse import parse_datetime
from datetime import date
from pprint import pprint


# m = []
# with open('d.json') as f:
#     m = json.load(f)

# Hit.objects.all().delete()

# print(m[0])
# for i in m:
#     i.pop('slug', None)
#     dt = parse_datetime(i.get('created'))
#     # print(datetime.datetime.strptime(i.get('created'), "%Y-%m-%d"))
#     h = Hit.objects.create(**i)
#     h.created = dt
#     h.save()

# h = Hit.objects.exclude(method='OPTIONS')
# .filter(path__icontains='/shop')


# q = h.values('path', 'created__date').annotate(
#     count=models.Count('path')
# ).order_by('-count')
# m = h.values('created__date').annotate(
#     top_path=models.Subquery(q.filter(created__date=models.OuterRef('created__date')).values('path'))
# )

# top_path=models.Subquery(
#     h.filter(created__date=models.OuterRef('created__date'))
#     # .values('path', 'created__date').annotate(count=models.Count('path'))
# )
# )

# print(m)


# i = h.aggregate(c=models.Min('session'))
# print(i)

# f = h.aggregate(c=models.Max('session'))
# print(f)

# d = h.filter(session=i.get('c')).count()
# print(d)
# r = h.filter(session=f.get('c')).count()
# print(r)
