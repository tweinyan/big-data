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

  def showImportantNotification(notification: Notification, importantPeopleInfo: Seq[String]): String = {
    notification match {
      case Email(email, _, _) if importantPeopleInfo.contains(email) =>
        "You got an email from special someone!"
      case SMS(number, _) if importantPeopleInfo.contains(number) =>
        "You got an SMS from special someone!"
      case other =>
        showNotification(other)
    }
  }

  def main(args: Array[String]): Unit = {
//    val someSms = SMS("12345", "Are you there?")
//    val someVoiceRecoding = VoiceRecording("Tom", "voicerecoding.org/id/123")
//    println(showNotification(someSms))
//    println(showNotification(someVoiceRecoding))
    val importantPeopleInfo = Seq("867-5309", "jenny@gmail.com")

    val someSms = SMS("867-5309", "Are you there?")
    val someVoiceRecording = VoiceRecording("Tom", "voicerecording.org/id/123")
    val importantEmail = Email("jenny@gmail.com", "Drinks tonight?", "I'm free after 5!")
    val importantSms = SMS("867-5309", "I'm here! Where are you?")

    println(showImportantNotification(importantEmail, importantPeopleInfo))
    println(showImportantNotification(someVoiceRecording, importantPeopleInfo))
    println(showImportantNotification(importantEmail, importantPeopleInfo))
    println(showImportantNotification(importantSms, importantPeopleInfo))
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