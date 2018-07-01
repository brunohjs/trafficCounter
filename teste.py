from random import randint

a = [randint(0,10) for i in range(10)]

print('antes: ',a)
i = 0
while i < len(a)-1:
    if a[i]-a[i+1] < 3:
        print(a[i], a[i+1])
        del(a[i])
        print(a)
        print()
    else:
        i += 1
print('depois: ',a)