class Base:
	def __init__(self,var1,var2):
		self.var1=var1
		self.var2=var2

	def getVar1(self):
		pass

	def getVar2(self):
		pass


class Derive1Add(Base):
	def __init__(self,var1,var2):
		Base.__init__(self,var1,var2)

	def getVar1(self):
		return self.var1
	
	def getVar2(self):
		return self.var2

	def Add(self):
		return self.var1 + self.var2

class Derive2Sub(Base):
	def __init__(self,var1,var2):
		Base.__init__(self,var1,var2)

	def getVar1(self):
		return self.var2
	
	def getVar2(self):
		return self.var1

	def Sub(self):
		return self.var1 - self.var2


def main():
	deriv1=Derive1Add(1,2)
	deriv2=Derive2Sub(1,2)
	base=[Base(1,2) for i in range(5)]
	base.append(deriv1)
	base.append(deriv2)
	print base[len(base)-2].Sub()

if __name__ == "__main__":
	main()
