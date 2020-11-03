solomeantest=function(x,mu)  #构造一个函数，X表示原始数据，mu表示已知的均值向量
{n=nrow(x) #定义n个样本
p=ncol(x) #定义P个指标
xbar=apply(x,2,mean)  #矩阵按列求均值
#apply是对x这个数据框在行或列的方向做指定操作（sum，mean，max，min等），1表示按行，2表示按列。
estvar=cov(x)  #协方差
HotelT=n*t(xbar-mu)%*%solve(estvar)%*%(xbar-mu) #构造T统计量，t(xbar-mu)表示转置，solve(estvar)表示协方差的逆矩阵
test=(n-p)/p/(n-1)*HotelT #构造检验统计量
pvalue=pf(test,p,n-p,lower.tail=F) #F检验，第一自由度为p，第二自由度为n-p；lower.tail = FALSE是大于一个数的概率，lower.tail = TRUE是算小于一个数的概率。
result=list(HotelT=HotelT,Ftest=test,pvalue=pvalue) #显示T值，F检验统计量，P值
return(result)
}


pairmeantest=function(x,y)  #构造新函数，x,y分别表示待检验的数据集
{
  p=ncol(x)
  n1=nrow(x)
  n2=nrow(y)
  xbar=apply(x,2,mean)
  ybar=apply(y,2,mean)
  xestvar=cov(x)
  yestvar=cov(y)
  xyestvar=((n1-1)*xestvar+(n2-1)*yestvar)/(n1+n2-2)
  HotelT=1/(1/n1+1/n2)*t(xbar-ybar)%*%solve(xyestvar)%*%(xbar-ybar)
  test=(n1+n2-p-1)/p/(n1+n2-2)*HotelT
  pvalue=pf(test,p,n1+n2-p-1,lower.tail=F)
  result=list(HotelT=HotelT,pvalue=pvalue)
  return(result)
}

setwd('C:/Users/Twisted/Desktop/多元第2章实验课-均值向量和协方差阵的检验')
library(readxl)
#2.4 不通过检验即 不拒绝 没有明显差异
x1<-read_xlsx('examp2.4.xlsx')
solomeantest(x1,c(4,50,10))

#2.5 p<0.05
x2<-read_xlsx('examp2.5.xlsx')
x2type1<-data.frame(x2[1:10,2:5])
x2type2<-data.frame(x2[11:20,2:5])
pairmeantest(x2type1,x2type2)
#test1
x3=read_xlsx('test1.xlsx')
solomeantest(x3,c(6212.01,32.87,2972,9.5,15.78))
#2.6
(mydata=read_xlsx("examp2.6.xlsx"))
attach(mydata)
fit=manova(cbind(x1,x2,x3,x4)~as.factor(group))
  summary.manova(fit,test="Wilks")
detach(x4)

