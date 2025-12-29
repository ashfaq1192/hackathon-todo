  File "/app/src/api/routes/tasks.py", line 99, in list_tasks
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 2275, in _fetchall_impl
    tasks = get_tasks_by_user(session, user_id)
    return list(self.iterator)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
           ^^^^^^^^^^^^^^^^^^^
  File "/app/src/database/crud.py", line 83, in get_tasks_by_user
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/orm/loading.py", line 220, in chunks
    tasks = session.exec(statement).all()
    fetch = cursor._raw_all_rows()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            ^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 1774, in all
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 541, in _raw_all_rows
    return self._allrows()
           ^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 548, in _allrows
    rows = self._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 1681, in _fetchall_impl
    return self._real_result._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    raise LookupError(
LookupError: 'medium' is not among the defined enum values. Enum name: taskpriority. Possible values: LOW, MEDIUM, HIGH
INFO:     100.64.0.4:54504 - "GET /api/rHHj1MQRNl56PF3oJMRvOQrcOuHkCOlJ/tasks HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
    return [make_row(row) for row in rows]
Traceback (most recent call last):
            ^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/sql/sqltypes.py", line 1709, in _object_value_for_elem
  File "lib/sqlalchemy/cyextension/resultproxy.pyx", line 22, in sqlalchemy.cyextension.resultproxy.BaseRow.__init__
  File "lib/sqlalchemy/cyextension/resultproxy.pyx", line 79, in sqlalchemy.cyextension.resultproxy._apply_processors
    return self._object_lookup[elem]  # type: ignore[return-value]
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/sql/sqltypes.py", line 1829, in process
    value = self._object_value_for_elem(value)
           ~~~~~~~~~~~~~~~~~~~^^^^^^
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'medium'
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/sql/sqltypes.py", line 1711, in _object_value_for_elem
The above exception was the direct cause of the following exception:
  File "/opt/venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
Traceback (most recent call last):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
  File "/opt/venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in __call__
    result = await app(  # type: ignore[func-returns-value]
    await super().__call__(scope, receive, send)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/opt/venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/middleware/cors.py", line 93, in __call__
    await self.simple_response(scope, receive, send, request_headers=headers)
  File "/opt/venv/lib/python3.12/site-packages/starlette/middleware/cors.py", line 144, in simple_response
    await self.app(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/opt/venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/opt/venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
    await route.handle(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
    await self.app(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/opt/venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
  File "/opt/venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 2525, in run_sync_in_worker_thread
    raise exc
  File "/opt/venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/opt/venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/anyio/to_thread.py", line 61, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    return await future
    return self._real_result._fetchall_impl()
           ^^^^^^^^^^^^
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 986, in run
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 2275, in _fetchall_impl
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/api/routes/tasks.py", line 99, in list_tasks
    tasks = get_tasks_by_user(session, user_id)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/database/crud.py", line 83, in get_tasks_by_user
    tasks = session.exec(statement).all()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 1774, in all
    return self._allrows()
           ^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 548, in _allrows
    rows = self._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/sqlalchemy/engine/result.py", line 1681, in _fetchall_impl
    return list(self.iterator)
           ^^^^^^^^^^^^^^^^^^^
