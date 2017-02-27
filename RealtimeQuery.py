import requests, json
from requestweather import fetchWeather

def query_realtime(city):
	'''query realtime weather'''
	r = fetchWeather(city)
	result = json.loads(r)
	temperature = result['results'][0]['now']['temperature']
	weather = result['results'][0]['now']['text']
#	get_weather = city + " " + weather + " " + temperature + "摄氏度"
	get_weather = {}
	get_weather[city] = [weather, temperature]
	log_append(city + str(get_weather[city][0]) + str(get_weather[city][1]))
	return get_weather

def documentation(filename):
	'''打印filename文档的内容'''
	with open(filename, "r", encoding = "utf-8") as f:
		return f.read()

def log():
	'''创建日志文件'''
	with open("log.txt", "w", encoding = "utf-8") as f:
		f.write("您的查询记录如下：\n")

def log_append(content):
	'''增加日志记录'''
	with open("log.txt", "a", encoding = "utf-8") as f:
		f.write(content + "\n")

if __name__ == "__main__":
	while True:
		user_input = input("请输入城市或指令：")

		if user_input in {"quit", "exit"}:
			break
		elif user_input == "history":
			print(documentation("log.txt"))
		elif user_input == "help":
			print(documentation("README.md"))
		else:
			print(query_realtime(user_input))



