from typing import Union, List, Dict

import uvicorn

from fastapi import FastAPI, status, Form, File, UploadFile
from pydantic import BaseModel, EmailStr
from fastapi.responses import HTMLResponse

app = FastAPI()


# 表单 form
# 要使用表单，需预先安装 python-multipart。

# Request body: application/x-www-form-urlencoded 回头补http协议
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


############################################################################
# 请求文件
# 因为上传文件以「表单数据」形式发送。
# 所以接收上传文件，要预先安装 python-multipart。


# 声明文件体必须使用 File，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数。
# 这种方式把文件的所有内容都存储在内存里，适用于小型文件。
# 不过，很多情况下，UploadFile 更好用。
@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# UploadFile 与 bytes 相比有更多优势：
# 使用 spooled 文件： (缓存?)
# 存储在内存的文件超出最大上限时，FastAPI 会把文件存入磁盘；
# 这种方式更适于处理图像、视频、二进制文件等大型文件，好处是不会占用所有内存；
# 可获取上传文件的元数据；
# 自带 file-like async 接口；
# 暴露的 Python SpooledTemporaryFile 对象，可直接传递给其他预期「file-like」对象的库。
# file-like 
# 对外提供面向文件 API 以使用下层资源的对象（带有 read() 或 write() 这样的方法）。
# 根据其创建方式的不同，文件对象可以处理对真实磁盘文件，对其他类型存储，
# 或是对通讯设备的访问（例如标准输入/输出、内存缓冲区、套接字、管道等等）。
# 文件对象也被称为 文件类对象 或 流。
# 实际上共有三种类别的文件对象: 原始 二进制文件, 缓冲 二进制文件 以及 文本文件。
# 它们的接口定义均在 io 模块中。创建文件对象的规范方式是使用 open() 函数。
# SpooledTemporaryFile
# 返回一个 file-like object （文件类对象）作为临时存储区域。
# 创建该文件使用了与 mkstemp() 相同的安全规则。
# 它将在关闭后立即销毁（包括垃圾回收机制关闭该对象时）。
# 在 Unix 下，该文件在目录中的条目根本不创建，或者创建文件后立即就被删除了，其他平台不支持此功能。
# 您的代码不应依赖使用此功能创建的临时文件名称，因为它在文件系统中的名称可能是可见的，也可能是不可见的。

# UploadFile 的属性如下：
# filename：上传文件名字符串（str），例如， myimage.jpg；
# content_type：内容类型（MIME 类型 / 媒体类型）字符串（str），例如，image/jpeg；
# file： SpooledTemporaryFile（ file-like 对象）。其实就是 Python文件，可直接传递给其他预期 file-like 对象的函数或支持库。
#
#  UploadFile 支持以下 async 方法，（使用内部 SpooledTemporaryFile）可调用相应的文件方法。
# write(data)：把 data （str 或 bytes）写入文件；
# read(size)：按指定数量的字节或字符（size (int)）读取文件内容；
# seek(offset)：移动至文件 offset （int）字节处的位置；
# 例如，await myfile.seek(0) 移动到文件开头；
# 执行 await myfile.read() 后，需再次读取已读取内容时，这种方法特别好用；
# close()：关闭文件。
# 因为上述方法都是 async 方法，要搭配「await」使用。
# 例如，在 async 路径操作函数 内，要用以下方式读取文件内容：
# contents = await myfile.read()

# 什么是 表单数据
# multipart/form-data
# https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods/POST

# 可在一个路径操作中声明多个 File 和 Form 参数，
# 但不能同时声明要接收 JSON 的 Body 字段。
# 因为此时请求体的编码是 multipart/form-data，
# 不是 application/json。

# 这不是 FastAPI 的问题，而是 HTTP 协议的规定。


# 可选上传
@app.post("/files2/")
async def create_file(file: bytes | None = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile2/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


# 带有额外元数据的 UploadFile
@app.post("/files3/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}


# 应该是用UploadFile方法上传File，带描述。
# 因为UploadFile没有description参数？ 不确定。
@app.post("/uploadfile3/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    return {"filename": file.filename}


# 多文件上传
# 可用同一个「表单字段」发送含多个文件的「表单数据」。
# 上传多个文件时，要声明含 bytes 或 UploadFile 的列表（List）
@app.post("/files4/")
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles4/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


# html页面格式 回头学
@app.get("/")
async def main():
    content = """
<body>
<form action="/files4/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles4/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)



# 带有额外元数据的多文件上传¶
# 和之前的方式一样, 您可以为 File() 设置额外参数, 即使是 UploadFile:
@app.post("/files5/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles5/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}


@app.get("/up")
async def main():
    content = """
<body>
<form action="/files5/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles5/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


# file and form
# bytes / UploadFile
@app.post("/files6/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

 
# 可在一个路径操作中声明多个 File 与 Form 参数，
# 但不能同时声明要接收 JSON 的 Body 字段。
# 因为此时请求体的编码为 multipart/form-data，
# 不是 application/json。













# ps 用这个的目的单纯是1902（

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_file_form:app', host="127.0.0.1", port=1902, reload=True, debug=True)

