import json
#写入json
user = {
    "name": "涛哥",
    "age":18 ,
    "gender":"男",
    "hobbies":["reading","swimming"]
}
with open("resources/user.json","w",encoding="utf-8") as f:
    #ensure_ascii:默认为True，即ASCII码的字符不进行转义（设置为False即进行转义）
    #indent:默认为None，即不进行缩进，这里设置为2，即缩进为2个空格
    json.dump(user,f,ensure_ascii=False,indent=2)


#读取json数据文件
with open("resources/user.json","r",encoding="utf-8") as f:
    user = json.load(f)
    print(user)
    print(type(user))




