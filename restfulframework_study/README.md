## django rest_framework demo
1. rest_framework 中的试图类是继承的 rest_framework.views.APIView, APIView 又继承的是 Django 原生的 View 类，在路由中都同样用了 as_view() 方法
2. 请求进来之后先走 self.dispatch() 方法，此方法在 APIView 中重写了，rest_framework 在此方法中实现了对扩展的调用
3. APIView 的 dispatch 函数都干了啥
    - 对 原生 request 对象进行加工，Request(request, parsers=self.get_parsers(), authenticators=self.get_authentictors(), negotiator=self.get_content_negotiator(), parser_context=parser_context)
    - 调用 self.initial(request, *args, **kwargs),这里面做了以下操作
        - 确认版本：确认 API 版本是否可用
        - 执行认证：对请求进行认证
        - 检查权限：检查请求的用户权限
        - 检查节流：对访问频率进行控制
    - 执行试图函数


此 demo 实现了**认证（基于token的认证）、权限、节流**
学习资料：https://www.cnblogs.com/wupeiqi/articles/7805382.html