# NewsScraper

This Python program scrapes french news from [LeMonde](https://www.lemonde.fr/) and spanish news from [ElMundo](https://www.elmundo.es/).
It parses top 3 articles from each website and sends them via email to specified address.

## Motivation

I am a big fan of learning languages. Speak 4 fluently so far: Kazakh, English, Spanish and Russian. Learning French for the last year. Started from 0 with the following great book [Easy French Step-by-Step](https://www.amazon.com/gp/product/0071453873/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1). After finishing it 2 times and conspecting everything I moved to awesome french comics [Les Aventures de Tintin](https://fr.wikipedia.org/wiki/Les_Aventures_de_Tintin). 
Generally, I would like to be aware of what is happening in the french and spanish speaking countries. So, I wrote this script using tutorial from [freeCodeCamp](https://www.freecodecamp.org/) and in particular following [video](https://www.youtube.com/watch?v=s8XjEuplx_U) by [Abdul](https://www.youtube.com/channel/UCpV_X0VrL8-jg3t6wYGS-1g).

## Stack

Program consists of following parts:
1. `Selenium` to imitate Chrome browser, navigate websites and get the data of interest. 
2. `email` to manage content of email.
3. `smtplib` to send email with the content.

