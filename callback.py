class Foo(object):
	def __init__(self):
		self._bar_observers =[]
	
	def add_bar_observers(self,observer):
		self._bar_observers.append(observer)

	def notify_bar(self,param):
		for observer in self._bar_observers:
			observer(param)
	
def observer(param):
	print "observer(%s)" %param

class Baz(object):
	def observer(self,param):
		print "Baz.observer(%s)" % param

class CallableClass(object):
	def __call__(self,param):
		print "CallableClass.__call__(%s)" %param

baz=Baz()
foo=Foo()

foo.add_bar_observers(observer)
foo.add_bar_observers(baz.observer)
foo.add_bar_observers(CallableClass())

foo.notify_bar(3)
