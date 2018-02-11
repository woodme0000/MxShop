# 之前我们有了snippets和users的端点，现在我们利用正则表达式和带@api_view基础视图函数创建初级的单一断点。
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'snippet': reverse('snippet:snippet_list', request=request, format=format),
        'snippet详情': reverse('snippet:snippet_detail', kwargs={"pk": 1}, request=request, format=format),
        '用户': reverse('snippet:user_list', request=request, format=format)
    })
