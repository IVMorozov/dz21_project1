
def get_main_menu(request):
    context = {
        'menu':[
            {'name': "Главная", 'url':'landing'},
            {'name': "О нас", 'url': 'about'},
            {'name': "Услуги", 'url': 'services_list'},
            {'name': "Мастера", 'url': 'masters_list'},
            {'name': "Отзывы", 'url': 'reviews'},
            # {'name': "Запись", 'url': 'make_appointment'},           

        ]
    }
    return context