# 2factorauth

Ein Modul zur 2Factor Authentifizierung

Diese Beispielapplikation implementiert eine Authentifizierung über zwei Schritte. Zunächst muss der Nutzer Login und Passwort eingeben. Danach wird ihm eine Email zugeschickt, in der sich eine zufällige achtstellige TAN befindet. Von dieser TAN muss der Nutzer auf der Folgeseite zwei Ziffern eingeben und ein Captcha richtig beantworten, um sich erfolgreich einzuloggen.

## Vorbereitung


### Email 

Für den Mailversand muss ein Mailserver im ZCML konfiguriert sein. Dazu bitte eine mail.zcml in das Paket legen mit folgendem Inhalt

<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:mail="http://namespaces.zope.org/mail">
  <mail:smtpMailer
    name="smtp"
    hostname="smtp.example.com"
    username="user@example.com"
    password="secret"
    port="25"
    /> 
  <mail:directDelivery 
    permission="zope.View"
    mailer="smtp" />
</configure>

### Captcha

Als Captchalösung wird Google's reCaptcha (https://www.google.com/recaptcha/intro/index.html) verwendet. D.h. zum Testen muss eine Internetverbindung bestehen. Für die Tests ist ein DEMO API Key konfiguriert und eingecheckt, der für localhost funktioniert. Soll das auf einem echten Domainnamen funktionieren, muss ein gesonderter API Key unter https://www.google.com/recaptcha/admin#list erzeugt werden.


## Beispielnutzung

Wenn neu installiert wurde, muss man zunächst eingeloggt als admin über den "Add a 2factor demo folder" link ein Verzeichnis mit eigenem Site Manager anlegen. Dieser benutzt dann das TwoFactorSessionCredentials Plugin. 

Es wird ebenfalls ein Testnutzer admin1:admin1 angelegt, der nur in diesem Unterverzeichnis existiert.

Als nächstes wieder als admin ausloggen.

Die Übersichtsseite unter http://localhost:8080 zeigt jetzt die "Existing Folders" an. Hier kann man den gerade angelegten Folder anspringen. Es erscheint ein Login Formular.

Hier kann man sich nun als admin1:admin1 einloggen und bekommt eine Email mit der TAN zugesendet (Achtung, mangels Userdatabase im Beispiel in auth.py hardgecoded). Zu Testzwecken wird die TAN auch auf der Console ausgegeben. Im Folgeformular werden nun 2 Stellen der TAN abgefragt, die in die beiden Felder TAN A und TAN B eingegeben werden müssen. Zusätzlich wird das Captcha angezeigt. 

Werden alle drei Felder korrekt ausgefüllt, ist der Benutzer eingeloggt.


## Todo

* Tests zum laufen bringen
* Edge Cases behandeln - (in manchen Fällen wie "TANs korrekt-Captcha fehlerhaft" ist die Fehlerbehandlung nicht funktional) 
* Code vereinfachen

* Integration in steg


## Noch zu tun

* Übersetzungen einbauen
* Automatische Sperre bei Falscheingaben (in Steg)
* Passwort Regel implementieren (in Steg)

