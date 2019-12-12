class Calc:
    def fn(self, a, b, c):
        return a + b * c


result = Calc().fn(1, 3, c=5)
print(result)
