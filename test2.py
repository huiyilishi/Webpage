#首先引入数据集x,和y的值的大小利用Python的数据结构：列表，来实现。
y=[4,8,13,35,34,67,78,89,100,101]
x=[0,1,2,3,4,5,6,7,8,9]
#然后再引入Python当中的绘图库，用于检测我们利用线性回归得到的结果是否正确
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=15)
import matplotlib.pyplot as plt
k = 0
for i in range(10):
    j = k
    k = j+i**2
    print(k)
    print(i)#实现计算x的平方
a11 = k
k=0
print("\n")#换行，使我们的结果更加清晰
for i in range(10):
#实现计算X的求和
    j = k
    k = j+i
    print(k)
a12 = k
#下面开始计算y*x的求和
k=0
for i in range(10):
    j = k
    k = j+y[i]*i
    print("我们k的大小是{}".format(k))
yixi = k
b1 = yixi
#现在再来计算我们yi求和后的大小

k=0
for i in range(10):
    j = k
    k = j+y[i]
    print(k)
yi = k
b2 = yi
#计算完毕，现在根据求出偏导数后的值计算我们斜率和截距的大小
#根据题意可得到：
a22 = 10
a21 = a12
#因此根据线性代数的克拉默法则，我们可以将其写成一个二阶行列式的形式：
print("现在开始打印行列式的各个值：")
print(a11)
print(a12)
print(a21)
print(a22)#检查无误后开始用克拉默法则进行计算

k = (b1*a22-a12*b2)/(a11*a22-a12*a21)
b = (a11*b2-a21*b1)/(a11*a22-a12*a21)
print("\n")
print("K的大小是：{}".format(k))
print("b的大小是：{}".format(b))
plt.scatter(x,y)
plt.title("利用最小二乘法实现线性单元回归",fontproperties=font)
plt.plot([0,12],[(a11*b2-a21*b1)/(a11*a22-a12*a21),((b1*a22-a12*b2)/(a11*a22-a12*a21))*12+b],linewidth=3,color="black")
plt.show()