# Misurda Scraper

## Purpose
I'm a UArizona student and my professor uses his own website over D2L. As a result, I don't get any notifications when new announcements/assignments are posted. One day it dawned on me -- I'm a Computer Science major performing the repetetive task of visiting a website daily (or more) to see if anything new was posted.

I spent a few hours writing this script to solve my problem. It scrapes the class website for announcements and tries to insert them into a MySQL database. If there is an error, the announcement is passed. If it goes in, then the announcement is assumed to be new and the text content of that announcement is texted to my phone via Twilio.

## Required Libraries
`BeautifulSoup`  
`requests`  
`twilio`  
`mysql-connector`

## Screenshots
![alt text](img/website.jpg "Class website")  
![alt text](img/text.jpg "Class website")
