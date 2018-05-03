package com.bigdataml.helloworld

/**
  * Created by tweinyan on 03/05/2018.
  */
object Test {
  def main(args: Array[String]): Unit = {
//    printStrings(22, "china", "us", "uk", "ak")

//    for(i<-1 to 10)
//      println(i+"的阶乘为: ="+method(i))

//    println(apply(layout, 20))

//    println(addData(4))

//    println(inc(444))

//    val logWith = log("my is", _:String)
//    logWith("m1")
//    logWith("m2")
//    logWith("m3")

//    println(add(2, 3))
//    println(rString("wo shi")("bigdata ml"))

    println(multiplier(2))
  }
  // 闭包
  var j = 4
  val multiplier=(i:Int)=>i*j

  // 函数柯里化
  def add(x:Int, y:Int):Int = x+y
  def rString(s1:String)(s2:String)={
    s1+s2
  }

  // 偏函数
  def log(info:String, message:String)={
    println(info+"-----"+message)
  }

  // 匿名函数
  var inc=(x:Int) => x + 1

  // 嵌套函数
  def addData(i:Int):Int={
    def addData1(i:Int, j:Int=7):Int={
      var sum:Int = i + j
      sum
    }
    addData1(i)
  }

  // 高阶函数
  def apply(f:Int =>String, v:Int):String={
    return f(v)
  }
  def layout[A](x:A)="["+x.toString()+"]"

  // 递归
  def method(n:Int):Int={
    if(n<=1)
      1
    else
      n * method(n-1)
  }

  // 多参数
  def printStrings(firstData:Int, args:String*)={
    println("firstData:" + firstData)
    var i:Int=0;
    for(arg<-args){
      println("Arg Value["+i+"]="+arg)
      i += 1
    }
  }
}
