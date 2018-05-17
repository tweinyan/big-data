/**
  * Created by tweinyan on 03/05/2018.
  */
object myfirstScala {
  class Point {
    private var _x = 0
    private var _y = 0
    private val bound = 100

    def x = _x

    def x_= (newValue: Int): Unit = {
      if (newValue < bound) _x = newValue else printWarning
    }

    def y = _y
    def y_= (newValue: Int): Unit = {
      if (newValue < bound) _y = newValue else printWarning
    }

    private def printWarning = println("WARNING: Out of bounds")
  }

  def main(args: Array[String]): Unit = {
    val point1 = new Point
    point1.x = 990
  }
  //def main(args: Array[String]): Unit = {
  //  noData
  //}
  //def addInt(a:Int, b:Int):Int={
  //  a + b
  //}
  //def noData:Unit={
  //  println("no data")
  //}
}
