document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.querySelector('#id_master');
    const servicesSelect = document.querySelector('#id_services');    

    // Функция для получения CSRF токена из cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    // if (masterSelect) {
    //     alert('первый этап');
    // }
    // if (servicesSelect) {
    //     alert('второй этап');
    // }


    if (masterSelect && servicesSelect) {
        // alert('первый этап');
        const updateServices = () => {
            const masterId = masterSelect.value;
            if (masterId) {
                fetch('/ajax/get-master-services/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ master_id: masterId })
                })
                .then(response => response.json())
                .then(data => {
                    servicesSelect.innerHTML = ''; // Очищаем список услуг
                    if (data.services) {
                        data.services.forEach(service => {
                            const option = document.createElement('option');
                            option.value = service.id;
                            option.textContent = service.description;
                            servicesSelect.appendChild(option);
                        });
                    }
                })
                .catch(error => console.error('Ошибка при загрузке услуг:', error));
            } else {
                servicesSelect.innerHTML = ''; // Очищаем, если мастер не выбран
            }
        };

        masterSelect.addEventListener('change', updateServices);
        // Вызываем функцию при загрузке страницы
        updateServices();
    }
});

// document.addEventListener('DOMContentLoaded', function() {
//     const header = document.querySelector('h1');
//     const masterSelect = document.querySelector('#id_master');
//     const servicesSelect = document.querySelector('#id_services');
//     masterSelect.addEventListener('change', function() {const masterId = this.value;})
    
//     if (header) {
//         header.addEventListener('click', function() {
//             alert('Вы кликнули по заголовку H1!', masterId);
//             alert('мастер');
//         });

//     } else {
//         console.error('Заголовок H1 не найден на странице.');
//     }
//     if (masterSelect) {        
//         masterSelect.addEventListener('click', function() {
//             alert('мастер');
//         });      
//     }
//     if (servicesSelect) {
//             alert('сервис');
//     }
// });

// document.addEventListener('DOMContentLoaded', function() {
//     const masterSelect = document.querySelector('#id_master');
//     const servicesSelect = document.querySelector('#id_services');

//     if (masterSelect && servicesSelect) {
//         masterSelect.addEventListener('change', function() {
//             const masterId = this.value;
//             if (masterId) {
//                 fetch(`/ajax/get-master-services/?master_id=${masterId}`)
//                     .then(response => response.json())
//                     .then(data => {
//                         servicesSelect.innerHTML = ''; // Очищаем список услуг
//                         if (data.services) {
//                             data.services.forEach(service => {
//                                 const option = document.createElement('option');
//                                 option.value = service.id;
//                                 option.textContent = service.description;
//                                 servicesSelect.appendChild(option);
//                             });
//                         }
//                     })
//                     .catch(error => console.error('Ошибка при загрузке услуг:', error));
//             } else {
//                 servicesSelect.innerHTML = ''; // Очищаем, если мастер не выбран
//             }
//         });

//         // Вызываем событие change при загрузке страницы, чтобы подгрузить услуги для мастера, выбранного по умолчанию
//         masterSelect.dispatchEvent(new Event('change'));
//     }
// });



// $(function() {
//     $( ".datepicker" ).datepicker({
//         changeMonth: true,
//         changeYear: true,
//         yearRange: "2025:2035",
//       // You can put more options here.
//     });
// });