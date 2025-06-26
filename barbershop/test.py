master = Master.objects.create(name= "Эльдар 'Бритва' Рязанов", phone='+7 (901) 123-45-67', address='Мой адрес не дом и не улица', experience=5)

master = Master.objects.create(name= "Зоя 'Ножницы' Космодемьянская", phone='+7 (902) 123-45-67', address='Мой адрес не дом и не улица', experience=4)

master = Master.objects.create(name= "Борис 'Фен' Пастернак", phone='+7 (903) 123-45-67', address='Мой адрес не дом и не улица', experience=3)

master = Master.objects.create(name= "Иннокентий 'Лак' Смоктуновский", phone='+7 (904) 123-45-67', address='Мой адрес не дом и не улица', experience=3)

master = Master.objects.create(name= "Раиса 'Бигуди' Горбачёва", phone='+7 (905) 123-45-67', address='Мой адрес не дом и не улица', experience=2)


order = Order.objects.create(client_name= "Пётр 'Безголовый' Головин", phone='+7 (905) 123-45-67', status='новая', appointment_date='2025-007-20')
master = Master.objects.get(pk=1)
order.master=master

services = Service.objects.get(pk=1)
order.services=services

order.save()


service = Service.objects.create(name= "'Горшок'", description="Стрижка под 'Горшок'", price=1000, duration=40 )

service = Service.objects.create(name= "'Взрыв на макаронной фабрике'", description="Укладка 'Взрыв на макаронной фабрике''", price=1100, duration=30 )

service = Service.objects.create(name= "Королевское бритье опасной бритвой", description="Королевское бритье опасной бритвой", price=1200, duration=20 )

service = Service.objects.create(name= "'Жизнь в розовом цвете'", description="Окрашивание 'Жизнь в розовом цвете'", price=1300, duration=120 )

service = Service.objects.create(name= "'Душ впечатлений'", description="Мытье головы 'Душ впечатлений'", price=1400, duration=10 )

service = Service.objects.create(name= "'Боярин'", description="Стрижка бороды 'Боярин'", price=1500, duration=30 )

service = Service.objects.create(name= "'Озарение'", description="Массаж головы 'Озарение''", price=1600, duration=40 )

service = Service.objects.create(name= "'Ветер в голове'", description="Укладка 'Ветер в голове'", price=1700, duration=80 )

service = Service.objects.create(name= "'Викинг'", description="Плетение косичек 'Викинг'", price=1800, duration=120 )

service = Service.objects.create(name= "Полировка лысины", description="Полировка лысины до блеска", price=1900, duration=15 )

 
