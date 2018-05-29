/**
  * Created by tweinyan on 03/05/2018.
  */
import scala.util.Random
object myfirstScala {
  abstract class Notification

  case class Email(sender: String, title: String, body: String) extends Notification
  case class SMS(caller: String, message: String) extends  Notification
  case class VoiceRecording(contactName: String, link: String) extends Notification

  def showNotification(notification: Notification): String = {
    notification match {
      case Email(email, title, _) =>
        s"You got an email from $email with title: $title"
      case SMS(number, message) =>
        s"You got an SMS from $number! Message: $message"
      case VoiceRecording(name, link) =>
        s"you received a Voice Recoding from $name! Click the link to hear it: $link"
    }
  }

  def main(args: Array[String]): Unit = {
    val someSms = SMS("12345", "Are you there?")
    val someVoiceRecoding = VoiceRecording("Tom", "voicerecoding.org/id/123")
    println(showNotification(someSms))
    println(showNotification(someVoiceRecoding))
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