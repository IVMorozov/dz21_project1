---
st_group: python 411
project: "[[Академия TOP]]"
journal: "[[PYTHON411]]"
tags:
  - PYTHON411
  - django
  - authentication
  - password-reset
  - email
  - forms
  - views
  - users
  - profile
date: 2025-07-27
type:
  - home work
hw_num: 31
topic: Рефакторинг проекта на классовые представления (CBV)
hw_theme:
  - django
  - authentication
  - password-reset
  - email
  - forms
  - views
  - UserCreationForm
  - AuthenticationForm
  - PasswordResetView
  - User
  - profile
links: [[PYTHON412 HW №48]]
---

# Домашнее задание 📃

**Полная система управления пользователями в Django: Аутентификация, Профиль и Восстановление пароля**

>[!info]
>
>### Краткое содержание
>
>В этом задании вы создадите полноценную систему управления пользователями с регистрацией, авторизацией, личным кабинетом и обязательным функционалом восстановления пароля через email. Система будет включать профиль пользователя с возможностью редактирования данных, смену пароля и полный цикл восстановления забытого пароля с отправкой email-уведомлений.

### Технологии: 🦾

- Python
- Django
- Django Authentication System
- Django Email Backend
- Django Forms & Views
- Bootstrap 5
- HTML/CSS Templates

## Задание 👷‍♂️

>[!warning]
> У вас может быть собственная система маршрутов и нейминг классов и шаблонов. Главное чтобы весь функционал был реализован.

### Настройка проекта и приложения

1. **Создание и настройка приложения**
   - Создайте новое приложение `users` в вашем проекте Django
   - Подключите `urls.py` из нового приложения в основной конфигурационный файл `urls.py`
   - Добавьте приложение `users` в список `INSTALLED_APPS` в `settings.py`

2. **Настройка email для восстановления пароля**
   - В `settings.py` настройте email backend для отправки писем в консоль:
     - `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
   - Добавьте настройки для корректной работы email системы

### Представления (Views)

3. **UserRegisterView**
   - **Родитель**: `django.views.generic.CreateView`
   - **Шаблон**: `users/register.html`
   - **Форма**: `UserRegisterForm`
   - Реализуйте автоматический вход пользователя после регистрации
   - Добавьте защиту от доступа аутентифицированных пользователей через `dispatch`
   - Настройте вывод сообщений об успехе/ошибке

4. **UserLoginView**
   - **Родитель**: `django.contrib.auth.views.LoginView`
   - **Шаблон**: `users/login.html`
   - **Форма**: `UserLoginForm`
   - Настройте `redirect_authenticated_user = True`
   - Реализуйте обработку параметра `next` для перенаправления
   - Добавьте сообщения об успешном входе и ошибках

5. **UserLogoutView**
   - **Родитель**: `django.contrib.auth.views.LogoutView`
   - Настройте перенаправление на главную страницу
   - Добавьте сообщение об успешном выходе

6. **UserProfileDetailView**
   - **Родитель**: `django.views.generic.DetailView`
   - **Шаблон**: `users/profile_detail.html`
   - **Миксин**: `LoginRequiredMixin`
   - Отображение профиля пользователя с проверкой принадлежности профиля

7. **UserProfileUpdateView**
   - **Родитель**: `django.views.generic.UpdateView`
   - **Шаблон**: `users/profile_update_form.html`
   - **Миксин**: `LoginRequiredMixin`
   - **Форма**: `UserProfileUpdateForm`
   - Позволяет редактировать только собственный профиль

8. **UserPasswordChangeView**
   - **Родитель**: `django.contrib.auth.views.PasswordChangeView`
   - **Шаблон**: `users/password_change_form.html`
   - **Миксин**: `LoginRequiredMixin`
   - **Форма**: `UserPasswordChangeForm`

>[!warning]
>
>### Обязательные представления для восстановления пароля
>
>Все четыре представления для восстановления пароля являются ОБЯЗАТЕЛЬНЫМИ для выполнения задания.

9. **CustomPasswordResetView**
   - **Родитель**: `django.contrib.auth.views.PasswordResetView`
   - **Шаблон**: `users/password_reset_form.html`
   - **Email-шаблон**: `users/password_reset_email.html`
   - **Форма**: `CustomPasswordResetForm`

10. **CustomPasswordResetDoneView**
    - **Родитель**: `django.contrib.auth.views.PasswordResetDoneView`
    - **Шаблон**: `users/password_reset_done.html`

11. **CustomPasswordResetConfirmView**
    - **Родитель**: `django.contrib.auth.views.PasswordResetConfirmView`
    - **Шаблон**: `users/password_reset_confirm.html`
    - **Форма**: `CustomSetPasswordForm`

12. **CustomPasswordResetCompleteView**
    - **Родитель**: `django.contrib.auth.views.PasswordResetCompleteView`
    - **Шаблон**: `users/password_reset_complete.html`

### Формы (Forms)

13. **UserLoginForm**
    - **Родитель**: `django.contrib.auth.forms.AuthenticationForm`
    - Настройте виджеты для полей `username` и `password` с классами Bootstrap 5
    - Добавьте placeholder'ы для улучшения UX

14. **UserRegisterForm**
    - **Родитель**: `django.contrib.auth.forms.UserCreationForm`
    - Добавьте обязательное поле `email` с валидацией
    - Настройте виджеты всех полей с классами Bootstrap 5
    - Уберите help_text для всех полей паролей и username

15. **UserProfileUpdateForm**
    - **Родитель**: `django.forms.ModelForm`
    - Поля: `username`, `email`, `avatar`, `birth_date`, `telegram_id`, `github_id`
    - Настройте виджеты с соответствующими типами полей (date для birth_date)

16. **UserPasswordChangeForm**
    - **Родитель**: `django.contrib.auth.forms.PasswordChangeForm`
    - Настройте виджеты для полей: `old_password`, `new_password1`, `new_password2`
    - Уберите help_text для всех полей

17. **CustomPasswordResetForm**
    - **Родитель**: `django.contrib.auth.forms.PasswordResetForm`
    - Настройте виджет для поля `email` с Bootstrap классами

18. **CustomSetPasswordForm**
    - **Родитель**: `django.contrib.auth.forms.SetPasswordForm`
    - Настройте виджеты для `new_password1` и `new_password2`
    - Уберите help_text для полей паролей

### Маршруты (URLs)

19. **Файл `urls.py` в приложении `users`**
    - `path('register/', UserRegisterView.as_view(), name='register')`
    - `path('login/', UserLoginView.as_view(), name='login')`
    - `path('logout/', UserLogoutView.as_view(), name='logout')`
    - `path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail')`
    - `path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit')`
    - `path('password_change/', UserPasswordChangeView.as_view(), name='password_change')`
    - `path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset')`
    - `path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done')`
    - `path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm')`
    - `path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete')`

### Шаблоны (Templates)

20. **Основные шаблоны аутентификации**
    - `users/register.html` - форма регистрации с ссылкой на вход
    - `users/login.html` - форма входа с ссылками на регистрацию и восстановление пароля
    - `users/profile_detail.html` - отображение профиля пользователя
    - `users/profile_update_form.html` - форма редактирования профиля
    - `users/password_change_form.html` - форма смены пароля

21. **Шаблоны восстановления пароля (ОБЯЗАТЕЛЬНО)**
    - `users/password_reset_form.html` - форма запроса восстановления пароля
    - `users/password_reset_done.html` - подтверждение отправки email
    - `users/password_reset_confirm.html` - форма установки нового пароля
    - `users/password_reset_complete.html` - подтверждение успешного сброса
    - `users/password_reset_email.html` - email-шаблон с ссылкой для восстановления

### Тестирование восстановления пароля

>[!warning]
>
>### Обязательное тестирование и скриншот
>
>После реализации функционала восстановления пароля вы ОБЯЗАТЕЛЬНО должны протестировать его работу и приложить скриншот email-сообщения из консоли Django. Скриншот должен показывать полное содержимое письма с ссылкой для восстановления пароля.

22. **Процедура тестирования**
    - Перейдите на страницу восстановления пароля
    - Введите email существующего пользователя
    - Проверьте консоль Django на наличие email-сообщения
    - Сделайте скриншот консоли с полным содержимым email
    - Скопируйте ссылку из email и перейдите по ней
    - Установите новый пароль и убедитесь в успешном входе

### Таблица компонентов

| Тип компонента | Название класса | Родительский класс | Маршрут | Шаблон/Форма |
|----------------|-----------------|-------------------|---------|--------------|
| **Views** | | | | |
| View | `UserRegisterView` | `CreateView` | `/register/` | `UserRegisterForm` |
| View | `UserLoginView` | `LoginView` | `/login/` | `UserLoginForm` |
| View | `UserLogoutView` | `LogoutView` | `/logout/` | - |
| View | `UserProfileDetailView` | `DetailView` + `LoginRequiredMixin` | `/profile/<int:pk>/` | - |
| View | `UserProfileUpdateView` | `UpdateView` + `LoginRequiredMixin` | `/profile/edit/` | `UserProfileUpdateForm` |
| View | `UserPasswordChangeView` | `PasswordChangeView` + `LoginRequiredMixin` | `/password_change/` | `UserPasswordChangeForm` |
| View | `CustomPasswordResetView` | `PasswordResetView` | `/password-reset/` | `CustomPasswordResetForm` |
| View | `CustomPasswordResetDoneView` | `PasswordResetDoneView` | `/password-reset/done/` | - |
| View | `CustomPasswordResetConfirmView` | `PasswordResetConfirmView` | `/reset/<uidb64>/<token>/` | `CustomSetPasswordForm` |
| View | `CustomPasswordResetCompleteView` | `PasswordResetCompleteView` | `/reset/done/` | - |
| **Forms** | | | | |
| Form | `UserLoginForm` | `AuthenticationForm` | - | - |
| Form | `UserRegisterForm` | `UserCreationForm` | - | - |
| Form | `UserProfileUpdateForm` | `ModelForm` | - | - |
| Form | `UserPasswordChangeForm` | `PasswordChangeForm` | - | - |
| Form | `CustomPasswordResetForm` | `PasswordResetForm` | - | - |
| Form | `CustomSetPasswordForm` | `SetPasswordForm` | - | - |
| **Templates** | | | | |
| Template | `register.html` | - | - | - |
| Template | `login.html` | - | - | - |
| Template | `profile_detail.html` | - | - | - |
| Template | `profile_update_form.html` | - | - | - |
| Template | `password_change_form.html` | - | - | - |
| Template | `password_reset_form.html` | - | - | - |
| Template | `password_reset_done.html` | - | - | - |
| Template | `password_reset_confirm.html` | - | - | - |
| Template | `password_reset_complete.html` | - | - | - |
| Template | `password_reset_email.html` | - | - | - |

>[!warning]
>
>### Критерии проверки 👌
>
>1. **Настройка проекта и базовый функционал (4 балла)**
>    - Приложение `users` создано, настроено и добавлено в `INSTALLED_APPS`.
>    - В `settings.py` корректно настроен `EMAIL_BACKEND` для вывода в консоль.
>    - Реализованы представления для регистрации, входа, выхода, просмотра и редактирования профиля, а также смены пароля (`UserRegisterView`, `UserLoginView`, `UserLogoutView`, `UserProfileDetailView`, `UserProfileUpdateView`, `UserPasswordChangeView`).
>    - Все соответствующие формы (`UserRegisterForm`, `UserLoginForm`, `UserProfileUpdateForm`, `UserPasswordChangeForm`) созданы, унаследованы от правильных классов и стилизованы с помощью виджетов и классов Bootstrap 5.
>
>2. **Реализация восстановления пароля (5 баллов)**
>    - Реализованы все четыре обязательных представления для сброса пароля (`CustomPasswordResetView`, `CustomPasswordResetDoneView`, `CustomPasswordResetConfirmView`, `CustomPasswordResetCompleteView`).
>    - Созданы и настроены кастомные формы `CustomPasswordResetForm` и `CustomSetPasswordForm`.
>    - Созданы все пять необходимых шаблонов для процесса восстановления, включая `users/password_reset_email.html`.
>    - Маршруты для восстановления пароля прописаны в `urls.py` и работают корректно.
>    - Весь цикл восстановления пароля полностью функционален.
>
>3. **Шаблоны и интерфейс (2 балла)**
>    - Созданы все HTML-шаблоны, требуемые по заданию.
>    - Шаблоны корректно наследуются от базового шаблона (если он есть).
>    - Формы и кнопки стилизованы с использованием Bootstrap 5, интерфейс выглядит аккуратно.
>    - Реализованы и корректно работают сообщения для пользователя (Django Messages Framework).
>
>4. **Тестирование и качество кода (1 балл)**
>    - К работе приложен обязательный скриншот письма для восстановления пароля из консоли.
>    - Код хорошо структурирован, следует принципам DRY. Нет закомментированного или лишнего кода.
