import redis
import time
import json


class Queue(object):
	def __init__(self, name, ip='127.0.0.1', port=6379):
		self.name = name
		self.ip = ip
		self.port = port
		self.redis = redis.Redis(
			ip, port, charset='utf-8', decode_responses=True)

	def add(self, data):
		oldData = self.redis.get(self.name)
		if oldData == None:
			oldData = []
		else:
			oldData = json.loads(oldData)
		oldData.append(data)
		return self.redis.set(self.name, json.dumps(oldData))
	
	def get(self):
		return json.loads(self.redis.get(self.name))

	def count(self):
		return len(self.get())

	def removeByIndex(self, index):
		data = self.get()
		try:
			del data[index]
		except Exception as e:
			pass
		return self.redis.set(self.name, json.dumps(data))
	
	def removeBy(self, elementValue, elementProp='id'):
		data = self.get()
		for key in data:
			if elementValue == key.get(elementProp):
				del data[data.index(key)]
		return self.redis.set(self.name, json.dumps(data))

	def removeEqual(self, rData):
		data = self.get()
		if rData in data:
			del data[data.index(rData)]
		return self.redis.set(self.name, json.dumps(data))

queue = Queue('queue15')
queue.add({'id': 1, 'name': 'Agustin'})
queue.add({'id': 2, 'name': 'Esteban'})
queue.add({'id': 3, 'name': 'Gonzalo'})
queue.add({'id': 4, 'name': 'Francisco'})
queue.add({'id': 5, 'name': 'Facundo'})
queue.add({'id': 6, 'name': 'Jorge'})

print(queue.get())
print(queue.count())
print(queue.removeBy(1))
print(queue.removeBy(1))
print(queue.removeBy('Francisco', 'name'))
print(queue.removeEqual({'id': 5, 'name': 'Facundo'}))
print(queue.removeByIndex(0))
